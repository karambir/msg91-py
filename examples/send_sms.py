#!/usr/bin/env python3
"""
Example script showing how to use the MSG91 Python client to send SMS
"""

import os
from msg91 import Client

# Get AUTH_KEY from environment variables
AUTH_KEY = os.environ.get("MSG91_AUTH_KEY")

if not AUTH_KEY:
    print("Please set the MSG91_AUTH_KEY environment variable")
    exit(1)

# Initialize client
client = Client(AUTH_KEY)

# Example: Send SMS
try:
    response = client.sms.send(
        template_id="your_template_id",
        mobile="9199XXXXXXXX",
        variables={"name": "John", "otp": "1234"},
        sender_id="SENDER"
    )
    print("SMS sent successfully!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending SMS: {e}")

# Example: Get template versions
try:
    template_versions = client.template.get("your_template_id")
    print(f"Template versions: {template_versions}")
except Exception as e:
    print(f"Error getting template versions: {e}")