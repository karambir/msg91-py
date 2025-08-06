"""
MSG91 Python Client library
"""

from msg91.client import Client
from msg91.exceptions import APIError, AuthenticationError, MSG91Exception, ValidationError
from msg91.resources.otp import OTPResource
from msg91.resources.sms import SMSResource
from msg91.resources.template import TemplateResource
from msg91.version import __version__

__all__ = [
    "Client",
    "MSG91Exception",
    "AuthenticationError",
    "ValidationError",
    "APIError",
    "SMSResource",
    "TemplateResource",
    "OTPResource",
    "__version__",
]
