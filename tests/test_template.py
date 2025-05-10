"""
Tests for the Template resource
"""

from unittest.mock import MagicMock

from msg91.resources.template import TemplateResource


def test_create_template():
    """Test creating a template"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.post.return_value = {
        "type": "success",
        "message": "Template created successfully",
        "data": {"id": "template_123"},
    }

    # Create Template resource and create template
    template = TemplateResource(http_client)
    response = template.create(
        template_name="Test Template",
        template_body="Welcome {{name}}!",
        sender_id="SENDER",
        sms_type="NORMAL",
    )

    # Verify HTTP client was called correctly
    http_client.post.assert_called_once()
    args, kwargs = http_client.post.call_args
    assert args[0] == "sms/addTemplate"

    # Check payload
    payload = kwargs.get("json_data", {})
    assert payload["template_name"] == "Test Template"
    assert payload["template"] == "Welcome {{name}}!"
    assert payload["sender_id"] == "SENDER"
    assert payload["smsType"] == "NORMAL"

    # Check response
    assert response["type"] == "success"
    assert response["message"] == "Template created successfully"
    assert response["data"]["id"] == "template_123"


def test_add_template_version():
    """Test adding a new version to a template"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.post.return_value = {
        "type": "success",
        "message": "Template version added successfully",
        "data": {"id": "version_123"},
    }

    # Create Template resource and add version
    template = TemplateResource(http_client)
    response = template.add_version(
        template_id="template_123",
        template_body="Welcome {{name}}! New version",
        sender_id="SENDER",
    )

    # Verify HTTP client was called correctly
    http_client.post.assert_called_once()
    args, kwargs = http_client.post.call_args
    assert args[0] == "sms/addTemplateVersion"

    # Check payload
    payload = kwargs.get("json_data", {})
    assert payload["template_id"] == "template_123"
    assert payload["template"] == "Welcome {{name}}! New version"
    assert payload["sender_id"] == "SENDER"

    # Check response
    assert response["type"] == "success"
    assert response["message"] == "Template version added successfully"
    assert response["data"]["id"] == "version_123"


def test_get_template_versions():
    """Test getting template versions"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.post.return_value = {
        "type": "success",
        "data": [
            {"id": "version_1", "template": "Welcome {{name}}! Version 1"},
            {"id": "version_2", "template": "Welcome {{name}}! Version 2"},
        ],
    }

    # Create Template resource and get versions
    template = TemplateResource(http_client)
    response = template.get("template_123")

    # Verify HTTP client was called correctly
    http_client.post.assert_called_once()
    args, kwargs = http_client.post.call_args
    assert args[0] == "sms/getTemplateVersions"

    # Check payload
    payload = kwargs.get("json_data", {})
    assert payload["template_id"] == "template_123"

    # Check response
    assert response["type"] == "success"
    assert len(response["data"]) == 2
    assert response["data"][0]["id"] == "version_1"
    assert response["data"][1]["id"] == "version_2"


def test_set_default_template():
    """Test setting a template version as default"""
    # Mock HTTP client
    http_client = MagicMock()
    http_client.get.return_value = {"type": "success", "message": "Template version set as default"}

    # Create Template resource and set default
    template = TemplateResource(http_client)
    response = template.set_default("template_123", "version_123")

    # Verify HTTP client was called correctly
    http_client.get.assert_called_once()
    args, kwargs = http_client.get.call_args
    assert args[0] == "sms/markActive"

    # Check params
    params = kwargs.get("params", {})
    assert params["template_id"] == "template_123"
    assert params["id"] == "version_123"

    # Check response
    assert response["type"] == "success"
    assert response["message"] == "Template version set as default"
