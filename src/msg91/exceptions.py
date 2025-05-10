"""
Exceptions for the MSG91 Python Library
"""

from typing import Any, Dict, Optional


class MSG91Exception(Exception):
    """Base exception for all MSG91 errors"""

    def __init__(
        self,
        message: str,
        status: Optional[int] = None,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status = status
        self.code = code
        self.details = details or {}
        super().__init__(message)


class AuthenticationError(MSG91Exception):
    """Authentication related errors"""

    pass


class ValidationError(MSG91Exception):
    """Validation errors related to request parameters"""

    pass


class APIError(MSG91Exception):
    """API errors returned by MSG91 service"""

    pass
