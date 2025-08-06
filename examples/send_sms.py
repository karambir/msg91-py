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

# Example 1: Send SMS using standard SMS API
try:
    response = client.sms.send(
        mobile="919XXXXXXXXX",  # Include country code
        message="Hello, this is a test message from MSG91!",
        sender="SENDER",  # Your approved sender ID
        route="4",  # 4 for transactional, 1 for promotional
        country="91",  # 91 for India, 0 for international
    )
    print("SMS sent successfully!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending SMS: {e}")

# Example 2: Send SMS to multiple numbers
try:
    response = client.sms.send(
        mobile=["919XXXXXXXXX", "919YYYYYYYYY"],  # Multiple numbers
        message="Bulk SMS message",
        sender="SENDER",
        route="4",
    )
    print("Bulk SMS sent successfully!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending bulk SMS: {e}")

# Example 3: Send SMS with optional parameters
try:
    response = client.sms.send(
        mobile="919XXXXXXXXX",
        message="This is a scheduled message!",
        sender="SENDER",
        route="4",
        scheduled_datetime="2025-12-25 10:00:00",  # Schedule for later
        campaign="MyCampaign",  # Campaign tracking
        flash=True,  # Flash SMS
        unicode=True,  # Unicode support
    )
    print("Scheduled SMS created successfully!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error scheduling SMS: {e}")

# Example 4: Send SMS using template (Flow API)
try:
    response = client.sms.send_template(
        template_id="your_template_id",
        mobile="919XXXXXXXXX",
        variables={"name": "John", "otp": "1234"},
        sender_id="SENDER",
    )
    print("Template SMS sent successfully!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error sending template SMS: {e}")

# Example 5: Get template versions
try:
    template_versions = client.template.get("your_template_id")
    print(f"Template versions: {template_versions}")
except Exception as e:
    print(f"Error getting template versions: {e}")
