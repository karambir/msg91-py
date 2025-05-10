"""
SMS Resource for MSG91 API
"""

from typing import Any, Dict, List, Optional, Union

from msg91.resources.base import BaseResource


class SMSResource(BaseResource):
    """Resource for sending SMS and managing SMS-related operations"""

    def send(
        self,
        template_id: str,
        mobile: Union[str, List[str]],
        variables: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
        short_url: Optional[bool] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send an SMS using a template

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
