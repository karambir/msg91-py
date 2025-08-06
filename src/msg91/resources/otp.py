"""
OTP Resource for MSG91 API
"""

from typing import Any, Dict, Optional

import httpx

from msg91.resources.base import BaseResource


class OTPResource(BaseResource):
    """Resource for OTP operations including send, verify, and resend"""

    def send(
        self,
        mobile: str,
        message: Optional[str] = None,
        sender: Optional[str] = None,
        otp: Optional[str] = None,
        otp_expiry: Optional[int] = None,
        otp_length: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send OTP to a mobile number

        Args:
            mobile: The mobile number to send OTP to (with country code)
            message: Custom OTP message (default: "Your verification code is ##OTP##")
            sender: Sender ID (default: SMSIND)
            otp: Specific OTP to send (auto-generated if not provided)
            otp_expiry: OTP expiry time in minutes (default: 1 day)
            otp_length: OTP digit count (4-9, default: 4)

        Returns:
            Response from the API containing session ID
        """
        # Use MSG91's SendOTP API endpoint
        otp_url = "http://api.msg91.com/api/sendotp.php"

        # Prepare parameters
        params: Dict[str, Any] = {
            "authkey": self.http_client.auth_key,
            "mobile": mobile,
        }

        if message:
            params["message"] = message

        if sender:
            params["sender"] = sender

        if otp:
            params["otp"] = otp

        if otp_expiry:
            params["otp_expiry"] = otp_expiry

        if otp_length:
            if not (4 <= otp_length <= 9):
                raise ValueError("OTP length must be between 4 and 9")
            params["otp_length"] = otp_length

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        try:
            response = httpx.get(otp_url, params=params, timeout=30)

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
                    response_data.get("message", "OTP sending failed")
                    if isinstance(response_data, dict)
                    else "OTP sending failed"
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

    def verify(
        self,
        mobile: str,
        otp: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Verify OTP for a mobile number

        Args:
            mobile: The mobile number to verify OTP for
            otp: The OTP to verify

        Returns:
            Response from the API indicating verification status
        """
        # Use MSG91's Verify OTP API endpoint
        verify_url = "http://api.msg91.com/api/verifyRequestOTP.php"

        # Prepare parameters
        params: Dict[str, Any] = {
            "authkey": self.http_client.auth_key,
            "mobile": mobile,
            "otp": otp,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        try:
            response = httpx.get(verify_url, params=params, timeout=30)

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
                    response_data.get("message", "OTP verification failed")
                    if isinstance(response_data, dict)
                    else "OTP verification failed"
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

    def resend(
        self,
        mobile: str,
        retrytype: str = "text",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Resend OTP to a mobile number

        Args:
            mobile: The mobile number to resend OTP to
            retrytype: Type of retry - "text", "voice" (default: "text")

        Returns:
            Response from the API
        """
        # Use MSG91's Retry OTP API endpoint
        retry_url = "http://api.msg91.com/api/retryotp.php"

        # Prepare parameters
        params: Dict[str, Any] = {
            "authkey": self.http_client.auth_key,
            "mobile": mobile,
            "retrytype": retrytype,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        try:
            response = httpx.get(retry_url, params=params, timeout=30)

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
                    response_data.get("message", "OTP resend failed")
                    if isinstance(response_data, dict)
                    else "OTP resend failed"
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
