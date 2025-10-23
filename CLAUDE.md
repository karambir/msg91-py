# MSG91 Python Client - Claude Development Guide

This document contains essential information about the MSG91 Python client library for AI assistants working on this codebase.

## Project Overview

**Project Name**: msg91-py
**Description**: A Python client library for the MSG91 SMS API
**Author**: Karambir Singh Nain
**License**: MIT
**Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
**Current Version**: 0.2.0

**Repository**: https://github.com/karambir/msg91-py
**PyPI Package**: `msg91-py` (import as `msg91`)

## Architecture & Structure

### Core Components

```
src/msg91/
├── __init__.py          # Main exports: Client, exceptions, __version__
├── client.py            # Main Client class (entry point)
├── http_client.py       # HTTPClient for API communication
├── exceptions.py        # Custom exception classes
├── version.py          # Version information
└── resources/
    ├── __init__.py
    ├── base.py         # BaseResource (parent class)
    ├── sms.py          # SMS operations
    └── template.py     # Template management
```

### Key Classes

1. **Client** (`client.py`): Main entry point
   - Initializes HTTPClient with auth_key
   - Provides access to `sms` and `template` resources

2. **HTTPClient** (`http_client.py`): Handles API communication
   - Base URL: `https://control.msg91.com/api/v5`
   - Uses httpx for HTTP requests
   - Handles authentication via `authkey` header
   - Implements error parsing and exception raising

3. **SMSResource** (`resources/sms.py`): SMS operations
   - `send()`: Standard SMS API (v2 endpoint)
   - `send_template()`: Template-based SMS (Flow API)
   - `get_logs()`: Retrieve SMS logs
   - `get_analytics()`: Get SMS analytics

4. **TemplateResource** (`resources/template.py`): Template management
   - `create()`: Create new templates
   - `add_version()`: Add template versions
   - `get()`: Get template versions
   - `set_default()`: Set default template version

## Development Environment

### Package Management
- **Primary**: `uv` (Python package manager)
- **Lock File**: `uv.lock`
- **Config**: `pyproject.toml`

### Development Tools

#### Code Quality
- **Linter/Formatter**: Ruff
  - Line length: 100 characters
  - Target Python: 3.9+
  - Rules: pycodestyle, pyflakes, isort, flake8-comprehensions, flake8-bugbear
  - Test files ignore E501 (line length)

#### Type Checking
- **Tool**: MyPy
- **Command**: `just typecheck` or `uv run mypy src`

#### Testing
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Additional**: pytest-sugar (enhanced output)
- **Config**: pytest.ini_options in pyproject.toml
- **Coverage Target**: src code under `msg91/` module

#### Pre-commit Hooks
- **Tool**: pre-commit
- **Config**: `.pre-commit-config.yaml`
- **Hooks**:
  - Basic file checks (trailing whitespace, yaml, toml, large files)
  - Security (detect private keys)
  - Ruff linting and formatting

### Build System
- **Backend**: Hatchling
- **Target**: Wheel packages from `src/msg91`

## Development Workflow

### Available Commands (via Justfile)

```bash
# Dependencies
just install        # Install with dev dependencies
just install-prod   # Production only
just lock           # Update uv.lock
just update         # Upgrade dependencies

# Code Quality
just lint           # Check formatting and linting
just format         # Auto-format code
just typecheck      # Run MyPy type checking
just check          # Run all quality checks (lint + typecheck + test)

# Testing
just test           # Run tests
just test-cov       # Run tests with coverage

# Building
just build          # Build package
just clean          # Clean build artifacts

# Pre-commit
just precommit-setup    # Install hooks
just precommit-run      # Run all hooks
```

### Code Standards

#### Import Organization
- Standard library imports
- Third-party imports (httpx, typing-extensions)
- Local imports (msg91.*)
- Use `from typing import` for type hints
- First-party module: `msg91`

#### Error Handling
- Custom exception hierarchy in `exceptions.py`:
  - `MSG91Exception` (base)
  - `AuthenticationError` (401 responses)
  - `ValidationError` (400 responses, validation type)
  - `APIError` (other HTTP errors)

#### HTTP Client Patterns
- Base URL: `https://control.msg91.com/api/v5` (for v5 APIs)
- Direct endpoints for v2 APIs: `http://api.msg91.com/api/v2/sendsms`
- Authentication: `authkey` header
- Content-Type: `application/json`
- Timeout: 30 seconds default

## SMS API Implementation

### Two SMS Sending Methods

1. **Standard SMS API** (`send()` method):
   - Endpoint: `http://api.msg91.com/api/v2/sendsms`
   - Direct httpx.post call (bypasses internal HTTP client)
   - Parameters: mobile, message, sender, route, country, flash, unicode, etc.
   - Supports bulk SMS (comma-separated mobile numbers)

2. **Template SMS API** (`send_template()` method):
   - Endpoint: `flow` (via internal HTTP client)
   - Uses template_id and variables
   - For backwards compatibility

### API Endpoints Used

#### SMS Operations
- **Send SMS**: `http://api.msg91.com/api/v2/sendsms` (v2 API)
- **Send Template**: `flow` (v5 API)
- **SMS Logs**: `report/logs/p/sms` (v5 API)
- **SMS Analytics**: `report/analytics/p/sms` (v5 API)

#### Template Operations
- **Create Template**: `sms/addTemplate` (v5 API)
- **Add Version**: `sms/addTemplateVersion` (v5 API)
- **Get Versions**: `sms/getTemplateVersions` (v5 API)
- **Set Default**: `sms/markActive` (v5 API)

## Testing Strategy

### Test Structure
```
tests/
├── test_client.py       # Client initialization and integration
├── test_sms.py         # SMS resource functionality
└── test_template.py    # Template resource functionality
```

### Test Patterns
- Mock httpx.Client.request for v5 APIs
- Mock httpx.post directly for v2 SMS API
- Test both success and error scenarios
- Verify request parameters and response handling
- Test exception raising for different error types

### Coverage Expectations
- Aim for high coverage on core functionality
- Current: ~82% overall coverage
- Focus on business logic in resources/

## Common Development Tasks

### Adding New API Endpoints
1. Add method to appropriate resource class
2. Use `self.http_client.post/get()` for v5 APIs
3. Handle errors with proper exception types
4. Add comprehensive tests
5. Update examples if user-facing

### Adding New Resources
1. Create new file in `resources/`
2. Inherit from `BaseResource`
3. Add to `Client` class initialization
4. Export in `resources/__init__.py`
5. Add tests in `tests/test_[resource].py`

### Running Quality Checks
Always run before committing:
```bash
just check  # Runs lint, typecheck, and tests
```

### Dependencies
- **Core**: httpx (HTTP client), typing-extensions (type hints)
- **Dev**: pytest, pytest-cov, mypy, ruff, pre-commit
- Keep dependencies minimal for production use

## API Authentication

- **Auth Method**: API Key via `authkey` header
- **Environment Variable**: `MSG91_AUTH_KEY` (used in examples)
- **Client Initialization**: `Client("your_auth_key")`

## Error Handling Patterns

```python
# Standard pattern for API errors
if not response.is_success:
    error_type = response_data.get("type", "").lower()
    message = response_data.get("message", "Operation failed")

    if response.status_code == 401:
        raise AuthenticationError(message=message, status=401, details=response_data)
    elif response.status_code == 400 or error_type == "validation":
        raise ValidationError(message=message, status=400, details=response_data)
    else:
        raise APIError(message=message, status=response.status_code, details=response_data)
```

## Deployment & Release

- **CI/CD**: GitHub Actions (`.github/workflows/ci.yml`)
- **Publishing**: PyPI as `msg91-py`
- **Versioning**: Update `src/msg91/version.py` and `pyproject.toml`
- **Build Command**: `just build`

This library provides a clean, well-tested interface to MSG91's SMS API with proper error handling, comprehensive testing, and modern Python development practices.
