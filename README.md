# MSG91 Python Client

A Python client library for the [MSG91 SMS API](https://docs.msg91.com/overview).

## Installation

```bash
pip install msg91
```

## Usage

### Initialize the client

```python
from msg91 import Client

# Initialize client with your auth key
client = Client("your_auth_key")
```

### Sending SMS

```python
# Send SMS using a template
response = client.sms.send(
    template_id="your_template_id",
    mobile="9199XXXXXXXX",
    variables={"var1": "value1", "var2": "value2"},
    sender_id="SENDER"
)
print(response)

# Send SMS to multiple recipients
response = client.sms.send(
    template_id="your_template_id",
    mobile=["9199XXXXXXXX", "9198XXXXXXXX"],
    variables={"var1": "value1", "var2": "value2"},
    sender_id="SENDER"
)
print(response)
```

### Managing Templates

```python
# Create a new template
response = client.template.create(
    template_name="Welcome",
    template_body="Welcome to our service, {{var1}}!",
    sender_id="SENDER",
    sms_type="NORMAL"  # Options: NORMAL, UNICODE
)
print(response)

# Get template versions
template_versions = client.template.get("template_id")
print(template_versions)

# Add a new version to an existing template
response = client.template.add_version(
    template_id="template_id",
    template_body="Welcome to our service, {{var1}}! New version.",
    sender_id="SENDER"
)
print(response)

# Set a template version as default
response = client.template.set_default(
    template_id="template_id",
    version_id="version_id"
)
print(response)
```

### Logs and Analytics

```python
# Get SMS logs
logs = client.sms.get_logs(
    start_date="2023-01-01",
    end_date="2023-01-31"
)
print(logs)

# Get analytics
analytics = client.sms.get_analytics()
print(analytics)

# Get analytics for specific date range
analytics = client.sms.get_analytics(
    start_date="2023-01-01",
    end_date="2023-01-31"
)
print(analytics)
```

## API Endpoints

The client uses the following MSG91 API endpoints:

- Send SMS: `flow`
- SMS Logs: `report/logs/p/sms`
- SMS Analytics: `report/analytics/p/sms`
- Create Template: `sms/addTemplate`
- Add Template Version: `sms/addTemplateVersion`
- Get Template Versions: `sms/getTemplateVersions`
- Mark Template as Default: `sms/markActive`

## Requirements

- Python 3.9+
- httpx

## License

This project is licensed under the MIT License - see the LICENSE file for details.