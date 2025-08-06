"""
Tests for OTP Resource
"""

from unittest.mock import MagicMock, patch

import pytest

from msg91 import Client
from msg91.exceptions import APIError, AuthenticationError, ValidationError


@pytest.fixture
def client():
    """Create a test client"""
    return Client("test_auth_key")


def test_send_otp_basic(client):
    """Test basic OTP sending"""
    with patch("httpx.get") as mock_get:
        # Mock successful response
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"type": "success", "message": "3763646c3058373530393938"}
        mock_get.return_value = mock_response

        response = client.otp.send(mobile="919999999999")

        # Verify request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "http://api.msg91.com/api/sendotp.php" in args
        assert kwargs["params"]["authkey"] == "test_auth_key"
        assert kwargs["params"]["mobile"] == "919999999999"

        # Verify response
        assert response["type"] == "success"
        assert "message" in response


def test_send_otp_with_options(client):
    """Test OTP sending with all options"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"type": "success", "message": "session_id"}
        mock_get.return_value = mock_response

        response = client.otp.send(
            mobile="919999999999",
            message="Your OTP is ##OTP##",
            sender="MYAPP",
            otp="1234",
            otp_expiry=5,
            otp_length=6,
        )

        # Verify request parameters
        args, kwargs = mock_get.call_args
        params = kwargs["params"]
        assert params["mobile"] == "919999999999"
        assert params["message"] == "Your OTP is ##OTP##"
        assert params["sender"] == "MYAPP"
        assert params["otp"] == "1234"
        assert params["otp_expiry"] == 5
        assert params["otp_length"] == 6

        assert response["type"] == "success"


def test_send_otp_invalid_length(client):
    """Test OTP sending with invalid length"""
    with pytest.raises(ValueError, match="OTP length must be between 4 and 9"):
        client.otp.send(mobile="919999999999", otp_length=3)

    with pytest.raises(ValueError, match="OTP length must be between 4 and 9"):
        client.otp.send(mobile="919999999999", otp_length=10)


def test_verify_otp(client):
    """Test OTP verification"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            "type": "success",
            "message": "OTP verified successfully",
        }
        mock_get.return_value = mock_response

        response = client.otp.verify(mobile="919999999999", otp="1234")

        # Verify request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "http://api.msg91.com/api/verifyRequestOTP.php" in args
        assert kwargs["params"]["authkey"] == "test_auth_key"
        assert kwargs["params"]["mobile"] == "919999999999"
        assert kwargs["params"]["otp"] == "1234"

        assert response["type"] == "success"


def test_resend_otp_text(client):
    """Test OTP resending via text"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"type": "success", "message": "OTP resent successfully"}
        mock_get.return_value = mock_response

        response = client.otp.resend(mobile="919999999999", retrytype="text")

        # Verify request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "http://api.msg91.com/api/retryotp.php" in args
        assert kwargs["params"]["authkey"] == "test_auth_key"
        assert kwargs["params"]["mobile"] == "919999999999"
        assert kwargs["params"]["retrytype"] == "text"

        assert response["type"] == "success"


def test_resend_otp_voice(client):
    """Test OTP resending via voice"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"type": "success", "message": "OTP resent via voice"}
        mock_get.return_value = mock_response

        response = client.otp.resend(mobile="919999999999", retrytype="voice")

        # Verify request was made correctly
        args, kwargs = mock_get.call_args
        params = kwargs["params"]
        assert params["retrytype"] == "voice"

        assert response["type"] == "success"


def test_send_otp_authentication_error(client):
    """Test OTP send with authentication error"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 401
        mock_response.json.return_value = {"type": "error", "message": "Invalid authentication key"}
        mock_get.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            client.otp.send(mobile="919999999999")

        assert exc_info.value.status == 401
        assert "Invalid authentication key" in str(exc_info.value)


def test_verify_otp_validation_error(client):
    """Test OTP verify with validation error"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"type": "error", "message": "Invalid OTP"}
        mock_get.return_value = mock_response

        with pytest.raises(ValidationError) as exc_info:
            client.otp.verify(mobile="919999999999", otp="wrong")

        assert exc_info.value.status == 400
        assert "Invalid OTP" in str(exc_info.value)


def test_resend_otp_api_error(client):
    """Test OTP resend with API error"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 500
        mock_response.json.return_value = {"type": "error", "message": "Server error"}
        mock_get.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            client.otp.resend(mobile="919999999999")

        assert exc_info.value.status == 500
        assert "Server error" in str(exc_info.value)


def test_send_otp_network_error(client):
    """Test OTP send with network error"""
    with patch("httpx.get", side_effect=Exception("Network error")):
        with pytest.raises(Exception, match="Network error"):
            client.otp.send(mobile="919999999999")


def test_send_otp_invalid_json_response(client):
    """Test OTP send with invalid JSON response"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid response"
        mock_get.return_value = mock_response

        response = client.otp.send(mobile="919999999999")

        assert response["raw_content"] == "Invalid response"


def test_otp_additional_kwargs(client):
    """Test OTP methods with additional kwargs"""
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"type": "success"}
        mock_get.return_value = mock_response

        # Test send with additional parameters
        client.otp.send(mobile="919999999999", extra_param="value", another_param="another_value")

        args, kwargs = mock_get.call_args
        params = kwargs["params"]
        assert params["extra_param"] == "value"
        assert params["another_param"] == "another_value"
