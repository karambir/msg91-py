"""
Template Resource for MSG91 API
"""

from typing import Any, Dict

from msg91.resources.base import BaseResource


class TemplateResource(BaseResource):
    """Resource for managing SMS templates"""

    def create(
        self,
        template_name: str,
        template_body: str,
        sender_id: str,
        sms_type: str = "NORMAL",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Create a new SMS template

        Args:
            template_name: Name of the template
            template_body: Content of the SMS template
            sender_id: Sender ID to use with this template
            sms_type: Type of SMS template (NORMAL, UNICODE)

        Returns:
            Response from the API
        """
        payload: Dict[str, Any] = {
            "template_name": template_name,
            "template": template_body,
            "sender_id": sender_id,
            "smsType": sms_type,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value

        return self.http_client.post("sms/addTemplate", json_data=payload)

    def add_version(
        self,
        template_id: str,
        template_body: str,
        sender_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Add a new version to an existing template

        Args:
            template_id: ID of the template to add a version to
            template_body: Content of the new template version
            sender_id: Sender ID to use with this template

        Returns:
            Response from the API
        """
        payload: Dict[str, Any] = {
            "template_id": template_id,
            "template": template_body,
            "sender_id": sender_id,
        }

        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value

        return self.http_client.post("sms/addTemplateVersion", json_data=payload)

    def get(self, template_id: str) -> Dict[str, Any]:
        """
        Get details of a specific template's versions

        Args:
            template_id: ID of the template to retrieve

        Returns:
            Template versions details
        """
        payload = {"template_id": template_id}
        return self.http_client.post("sms/getTemplateVersions", json_data=payload)

    def set_default(self, template_id: str, version_id: str) -> Dict[str, Any]:
        """
        Mark a template version as default

        Args:
            template_id: ID of the template
            version_id: ID of the version to mark as default

        Returns:
            Response from the API
        """
        params = {"template_id": template_id, "id": version_id}
        return self.http_client.get("sms/markActive", params=params)
