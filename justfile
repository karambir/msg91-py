# MSG91 Python client development tasks
# Install 'just' from https://github.com/casey/just

# List all available recipes
default:
    @just --list

# Install development dependencies using uv
install:
    uv sync --frozen --group dev

# Install only the package without dev dependencies
install-prod:
    uv sync --frozen --no-dev

# Create/update uv.lock file from pyproject.toml
lock:
    uv lock

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=msg91 --cov-report=term-missing

# Update dependencies using uv and regenerate lock file
update:
    uv lock --upgrade

# Run code quality tools
lint:
    uv run ruff check src tests

# Format code
format:
    uv run ruff format src tests

# Check types with mypy
typecheck:
    uv run mypy src

# Build the package
build:
    uv build

# Clean build artifacts
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    find . -type d -name __pycache__ -exec rm -rf {} +

# Run all quality checks
check: lint typecheck test