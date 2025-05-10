"""
Base resource class for MSG91 API resources
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msg91.http_client import HTTPClient


class BaseResource:
    """Base class for all API resources"""

    def __init__(self, http_client: "HTTPClient"):
        self.http_client = http_client
