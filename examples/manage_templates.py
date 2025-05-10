#!/usr/bin/env python3
"""
Example script showing how to use the MSG91 Python client to manage templates
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

# Example: Create a new template
try:
    response = client.template.create(
        template_name="Welcome Message",
        template_body="Welcome to our service, {{name}}! Your OTP is {{otp}}.",
        sender_id="SENDER",
        sms_type="NORMAL"
    )
    print("Template created successfully!")
    print(f"Response: {response}")

    # Get template ID from response
    template_id = response.get("data", {}).get("id")

    if template_id:
        # Example: Add a new version to the template
        version_response = client.template.add_version(
            template_id=template_id,
            template_body="Welcome to our updated service, {{name}}! Your OTP is {{otp}}.",
            sender_id="SENDER"
        )
        print("Template version added successfully!")
        print(f"Version response: {version_response}")

        # Get template versions
        versions = client.template.get(template_id)
        print(f"Template versions: {versions}")

        # Example: Set a template version as default
        # Assuming we have a version ID from the versions response
        if versions and "data" in versions and len(versions["data"]) > 0:
            version_id = versions["data"][0].get("id")
            if version_id:
                default_response = client.template.set_default(
                    template_id=template_id,
                    version_id=version_id
                )
                print("Template version set as default!")
                print(f"Default response: {default_response}")

except Exception as e:
    print(f"Error managing templates: {e}")