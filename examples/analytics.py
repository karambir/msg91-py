#!/usr/bin/env python3
"""
Example script showing how to use the MSG91 Python client to get SMS logs and analytics
"""

import os
from datetime import datetime, timedelta
from msg91 import Client

# Get AUTH_KEY from environment variables
AUTH_KEY = os.environ.get("MSG91_AUTH_KEY")

if not AUTH_KEY:
    print("Please set the MSG91_AUTH_KEY environment variable")
    exit(1)

# Initialize client
client = Client(AUTH_KEY)

# Calculate date range for last 30 days
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# Example: Get SMS logs
try:
    logs = client.sms.get_logs(
        start_date=start_date,
        end_date=end_date
    )
    print(f"SMS Logs for {start_date} to {end_date}:")
    for log in logs.get("data", []):
        print(f"- Mobile: {log.get('mobile')}, Status: {log.get('status')}, Date: {log.get('date')}")
except Exception as e:
    print(f"Error getting SMS logs: {e}")

# Example: Get analytics
try:
    analytics = client.sms.get_analytics(
        start_date=start_date,
        end_date=end_date
    )
    print(f"\nSMS Analytics for {start_date} to {end_date}:")
    data = analytics.get("data", {})
    print(f"- Total sent: {data.get('total_sent', 0)}")
    print(f"- Delivered: {data.get('delivered', 0)}")
    print(f"- Failed: {data.get('failed', 0)}")
    print(f"- Pending: {data.get('pending', 0)}")
except Exception as e:
    print(f"Error getting analytics: {e}")