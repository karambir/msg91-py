"""
Tests for the SMS resource
"""

from unittest.mock import MagicMock

from msg91.resources.sms import SMSResource


def test_format_recipients_single():
    """Test formatting a single recipient"""
    http_client = MagicMock()
    sms = SMSResource(http_client)

    # Test with single mobile number
    recipients = sms._format_recipients("9199XXXXXXXX")
    assert len(recipients) == 1
    assert recipients[0]["mobile"] == "9199XXXXXXXX"
    assert "variables" not in recipients[0]

    # Test with single mobile number and variables
    variables = {"name": "Test User", "otp": "1234"}
    recipients = sms._format_recipients("9199XXXXXXXX", variables)
    assert len(recipients) == 1
    assert recipients[0]["mobile"] == "9199XXXXXXXX"
    assert recipients[0]["variables"] == variables


def test_format_recipients_multiple():
    """Test formatting multiple recipients"""
    http_client = MagicMock()
    sms = SMSResource(http_client)

    # Test with multiple mobile numbers
    recipients = sms._format_recipients(["9199XXXXXXXX", "9198XXXXXXXX"])
    assert len(recipients) == 2
    assert recipients[0]["mobile"] == "9199XXXXXXXX"
    assert recipients[1]["mobile"] == "9198XXXXXXXX"

    # Test with multiple mobile numbers and variables
    variables = {"name": "Test User", "otp": "1234"}
    recipients = sms._format_recipients(["9199XXXXXXXX", "9198XXXXXXXX"], variables)
    assert len(recipients) == 2
    assert recipients[0]["mobile"] == "9199XXXXXXXX"
    assert recipients[0]["variables"] == variables
    assert recipients[1]["mobile"] == "9198XXXXXXXX"
    assert recipients[1]["variables"] == variables


def test_send_sms():
    """Test sending SMS"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.post.return_value = {"type": "success", "message": "SMS sent successfully"}

    # Create SMS resource and send SMS
    sms = SMSResource(http_client)
    response = sms.send(
        template_id="test_template",
        mobile="9199XXXXXXXX",
        variables={"name": "Test User"},
        sender_id="SENDER",
        short_url=True,
    )

    # Verify HTTP client was called correctly
    http_client.post.assert_called_once()
    args, kwargs = http_client.post.call_args
    assert args[0] == "flow"

    # Check payload
    payload = kwargs.get("json_data", {})
    assert payload["template_id"] == "test_template"
    assert len(payload["recipients"]) == 1
    assert payload["recipients"][0]["mobile"] == "9199XXXXXXXX"
    assert payload["recipients"][0]["variables"] == {"name": "Test User"}
    assert payload["sender"] == "SENDER"
    assert payload["short_url"] == "1"

    # Check response
    assert response == {"type": "success", "message": "SMS sent successfully"}


def test_get_logs():
    """Test getting SMS logs"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.post.return_value = {"type": "success", "data": []}

    # Create SMS resource and get logs
    sms = SMSResource(http_client)
    response = sms.get_logs(start_date="2023-01-01", end_date="2023-01-31")

    # Verify HTTP client was called correctly
    http_client.post.assert_called_once()
    args, kwargs = http_client.post.call_args
    assert args[0] == "report/logs/p/sms"

    # Check payload
    payload = kwargs.get("json_data", {})
    assert payload["start_date"] == "2023-01-01"
    assert payload["end_date"] == "2023-01-31"

    # Check response
    assert response == {"type": "success", "data": []}


def test_get_analytics():
    """Test getting SMS analytics"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.get.return_value = {
        "type": "success",
        "data": {"total_sent": 100, "delivered": 90, "failed": 10},
    }

    # Create SMS resource and get analytics
    sms = SMSResource(http_client)
    response = sms.get_analytics(start_date="2023-01-01", end_date="2023-01-31")

    # Verify HTTP client was called correctly
    http_client.get.assert_called_once()
    args, kwargs = http_client.get.call_args
    assert args[0] == "report/analytics/p/sms"

    # Check params
    params = kwargs.get("params", {})
    assert params["start_date"] == "2023-01-01"
    assert params["end_date"] == "2023-01-31"

    # Check response
    assert response["type"] == "success"
    assert response["data"]["total_sent"] == 100
    assert response["data"]["delivered"] == 90
    assert response["data"]["failed"] == 10
