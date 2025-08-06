"""
MSG91 API Resources
"""

from msg91.resources.otp import OTPResource
from msg91.resources.sms import SMSResource
from msg91.resources.template import TemplateResource

__all__ = ["SMSResource", "TemplateResource", "OTPResource"]
