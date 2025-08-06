"""
OTP Resource for MSG91 API
"""

from typing import Any, Dict, Optional

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
        # Prepare parameters
        params: Dict[str, Any] = {
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

        # Use MSG91's SendOTP API endpoint
        return self.http_client.get("sendotp.php", params=params, api_version="v2")

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
        # Prepare parameters
        params: Dict[str, Any] = {
            "mobile": mobile,
            "otp": otp,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        # Use MSG91's Verify OTP API endpoint
        return self.http_client.get("verifyRequestOTP.php", params=params, api_version="v2")

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
        # Prepare parameters
        params: Dict[str, Any] = {
            "mobile": mobile,
            "retrytype": retrytype,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            params[key] = value

        # Use MSG91's Retry OTP API endpoint
        return self.http_client.get("retryotp.php", params=params, api_version="v2")
