"""
Tests for the MSG91 client
"""

from unittest.mock import MagicMock, patch

import pytest

from msg91.client import Client
from msg91.exceptions import APIError, AuthenticationError, ValidationError


def test_client_initialization():
    """Test client initialization with proper parameters"""
    client = Client("test_auth_key")
    assert client.http_client.auth_key == "test_auth_key"
    assert client.http_client.base_url == "https://control.msg91.com/api/v5"

    # Test with custom base URL
    custom_url = "https://custom.msg91.com/api"
    client = Client("test_auth_key", base_url=custom_url)
    assert client.http_client.base_url == custom_url

    # Test with custom timeout
    client = Client("test_auth_key", timeout=60)
    assert client.http_client.timeout == 60


@patch("httpx.Client.request")
def test_sms_send(mock_request):
    """Test SMS send functionality"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.is_success = True
    mock_response.json.return_value = {"type": "success", "message": "SMS sent successfully"}
    mock_request.return_value = mock_response

    # Initialize client and send SMS
    client = Client("test_auth_key")
    response = client.sms.send(
        template_id="test_template",
        mobile="9199XXXXXXXX",
        variables={"name": "Test User"},
        sender_id="SENDER",
    )

    # Verify request
    mock_request.assert_called_once()

    # Check method, url and headers
    args, kwargs = mock_request.call_args
    assert args[0] == "POST"
    assert args[1].endswith("flow")
    assert kwargs["headers"]["authkey"] == "test_auth_key"

    # Check JSON payload
    payload = kwargs["json"]
    assert payload["template_id"] == "test_template"
    assert len(payload["recipients"]) == 1
    assert payload["recipients"][0]["mobile"] == "9199XXXXXXXX"
    assert payload["recipients"][0]["variables"] == {"name": "Test User"}
    assert payload["sender"] == "SENDER"

    # Check response
    assert response == {"type": "success", "message": "SMS sent successfully"}


@patch("httpx.Client.request")
def test_template_create(mock_request):
    """Test template create functionality"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.is_success = True
    mock_response.json.return_value = {
        "type": "success",
        "message": "Template created",
        "data": {"id": "template_id_123"},
    }
    mock_request.return_value = mock_response

    # Initialize client and create template
    client = Client("test_auth_key")
    response = client.template.create(
        template_name="Test Template",
        template_body="This is a test template for {{name}}",
        sender_id="SENDER",
        sms_type="NORMAL",
    )

    # Verify request
    mock_request.assert_called_once()

    # Check method, url and headers
    args, kwargs = mock_request.call_args
    assert args[0] == "POST"
    assert args[1].endswith("sms/addTemplate")
    assert kwargs["headers"]["authkey"] == "test_auth_key"

    # Check JSON payload
    payload = kwargs["json"]
    assert payload["template_name"] == "Test Template"
    assert payload["template"] == "This is a test template for {{name}}"
    assert payload["sender_id"] == "SENDER"
    assert payload["smsType"] == "NORMAL"

    # Check response
    assert response["type"] == "success"
    assert response["message"] == "Template created"
    assert response["data"]["id"] == "template_id_123"


@patch("httpx.Client.request")
def test_authentication_error(mock_request):
    """Test authentication error handling"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.is_success = False
    mock_response.status_code = 401
    mock_response.json.return_value = {"type": "error", "message": "Invalid auth key"}
    mock_request.return_value = mock_response

    # Initialize client and attempt request
    client = Client("invalid_auth_key")

    # Verify authentication error is raised
    with pytest.raises(AuthenticationError) as exc_info:
        client.sms.send(template_id="test_template", mobile="9199XXXXXXXX")

    assert "Invalid auth key" in str(exc_info.value)
    assert exc_info.value.status == 401


@patch("httpx.Client.request")
def test_validation_error(mock_request):
    """Test validation error handling"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.is_success = False
    mock_response.status_code = 400
    mock_response.json.return_value = {"type": "validation", "message": "Invalid mobile number"}
    mock_request.return_value = mock_response

    # Initialize client and attempt request
    client = Client("test_auth_key")

    # Verify validation error is raised
    with pytest.raises(ValidationError) as exc_info:
        client.sms.send(template_id="test_template", mobile="invalid_mobile")

    assert "Invalid mobile number" in str(exc_info.value)
    assert exc_info.value.status == 400


@patch("httpx.Client.request")
def test_api_error(mock_request):
    """Test generic API error handling"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.is_success = False
    mock_response.status_code = 500
    mock_response.json.return_value = {"type": "error", "message": "Internal server error"}
    mock_request.return_value = mock_response

    # Initialize client and attempt request
    client = Client("test_auth_key")

    # Verify API error is raised
    with pytest.raises(APIError) as exc_info:
        client.sms.send(template_id="test_template", mobile="9199XXXXXXXX")

    assert "Internal server error" in str(exc_info.value)
    assert exc_info.value.status == 500
