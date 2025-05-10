"""
MSG91 Client for Python
"""

from typing import Any, Optional

from msg91.http_client import HTTPClient
from msg91.resources.sms import SMSResource
from msg91.resources.template import TemplateResource


class Client:
    """
    MSG91 API Client

    Args:
        auth_key: Your MSG91 authentication key
        base_url: Custom API base URL (optional)
        timeout: Request timeout in seconds (default: 30)
        **httpx_kwargs: Additional keyword arguments for httpx.Client
    """

    def __init__(
        self,
        auth_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **httpx_kwargs: Any,
    ):
        self.http_client = HTTPClient(
            auth_key=auth_key,
            base_url=base_url,
            timeout=timeout,
            **httpx_kwargs,
        )

        # Initialize resources
        self.sms = SMSResource(self.http_client)
        self.template = TemplateResource(self.http_client)
