"""
SMS Resource for MSG91 API
"""

from typing import Any, Dict, List, Optional, Union

import httpx

from msg91.resources.base import BaseResource


class SMSResource(BaseResource):
    """Resource for sending SMS and managing SMS-related operations"""

    def send(
        self,
        mobile: Union[str, List[str]],
        message: str,
        sender: str,
        route: str = "4",
        country: Optional[str] = None,
        flash: Optional[bool] = None,
        unicode: Optional[bool] = None,
        scheduled_datetime: Optional[str] = None,
        campaign: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send SMS using MSG91 API

        Args:
            mobile: The mobile number(s) to send SMS to (with country code)
            message: The SMS message content
            sender: The sender ID to use for sending SMS
            route: SMS route (1 for promotional, 4 for transactional)
            country: Country code (0 for international, 91 for India)
            flash: Whether to send as flash SMS
            unicode: Whether to send as unicode SMS
            scheduled_datetime: Schedule SMS for specific time
            campaign: Campaign name for tracking

        Returns:
            Response from the API
        """
        # Use MSG91's v2 SMS API endpoint
        sms_url = "http://api.msg91.com/api/v2/sendsms"

        # Format mobile numbers
        if isinstance(mobile, list):
            mobile_str = ",".join(mobile)
        else:
            mobile_str = mobile

        # Prepare payload
        payload: Dict[str, Any] = {
            "authkey": self.http_client.auth_key,
            "mobiles": mobile_str,
            "message": message,
            "sender": sender,
            "route": route,
            "response": "json",
        }

        if country is not None:
            payload["country"] = country

        if flash is not None:
            payload["flash"] = "1" if flash else "0"

        if unicode is not None:
            payload["unicode"] = "1" if unicode else "0"

        if scheduled_datetime:
            payload["scheduledatetime"] = scheduled_datetime

        if campaign:
            payload["campaign"] = campaign

        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value

        # Use direct httpx client for MSG91 v2 API
        headers = {
            "Content-Type": "application/json",
            "authkey": self.http_client.auth_key,
        }

        try:
            response = httpx.post(sms_url, json=payload, headers=headers, timeout=30)

            try:
                response_data = response.json()
            except ValueError:
                response_data = {"raw_content": response.text}

            if not response.is_success:
                from msg91.exceptions import APIError, AuthenticationError, ValidationError

                error_type = (
                    response_data.get("type", "").lower() if isinstance(response_data, dict) else ""
                )
                message = (
                    response_data.get("message", "SMS sending failed")
                    if isinstance(response_data, dict)
                    else "SMS sending failed"
                )

                if response.status_code == 401:
                    raise AuthenticationError(
                        message=message,
                        status=response.status_code,
                        details=response_data,
                    )
                elif response.status_code == 400 or error_type == "validation":
                    raise ValidationError(
                        message=message,
                        status=response.status_code,
                        details=response_data,
                    )
                else:
                    raise APIError(
                        message=message,
                        status=response.status_code,
                        details=response_data,
                    )

            return response_data

        except httpx.RequestError as e:
            from msg91.exceptions import MSG91Exception

            raise MSG91Exception(f"Network error: {str(e)}") from e

    def send_template(
        self,
        template_id: str,
        mobile: Union[str, List[str]],
        variables: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
        short_url: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an SMS using a template (Flow API)

        Args:
            template_id: The template ID to use for sending SMS
            mobile: The mobile number(s) to send SMS to
            variables: Template variables for substitution
            sender_id: The sender ID to use for sending SMS
            short_url: Whether to use short URLs in the SMS

        Returns:
            Response from the API
        """
        payload: Dict[str, Any] = {
            "template_id": template_id,
            "recipients": self._format_recipients(mobile, variables),
        }

        if sender_id:
            payload["sender"] = sender_id

        if short_url is not None:
            payload["short_url"] = "1" if short_url else "0"

        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value

        return self.http_client.post("flow", json_data=payload)

    def _format_recipients(
        self, mobile: Union[str, List[str]], variables: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Format recipients for the API payload"""
        if isinstance(mobile, str):
            mobile = [mobile]

        recipients = []
        for number in mobile:
            recipient: Dict[str, Any] = {"mobile": number}
            if variables:
                recipient["variables"] = variables
            recipients.append(recipient)

        return recipients

    def get_logs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get SMS logs

        Args:
            start_date: Start date for filtering (YYYY-MM-DD)
            end_date: End date for filtering (YYYY-MM-DD)

        Returns:
            SMS logs response
        """
        payload: Dict[str, Any] = {}

        if start_date:
            payload["start_date"] = start_date

        if end_date:
            payload["end_date"] = end_date

        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value

        return self.http_client.post("report/logs/p/sms", json_data=payload)

    def get_analytics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Get SMS analytics

        Args:
            start_date: Start date for analytics (YYYY-MM-DD)
            end_date: End date for analytics (YYYY-MM-DD)

        Returns:
            SMS analytics response
        """
        params: Dict[str, Any] = {}

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        return self.http_client.get("report/analytics/p/sms", params=params)
