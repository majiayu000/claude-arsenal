.PHONY: dev test lint fmt typecheck check clean sync upgrade

# Run development server
dev:
	uv run uvicorn myapp.main:app --reload

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=myapp --cov-report=html --cov-report=term

# Lint code
lint:
	uv run ruff check src tests

# Format code
fmt:
	uv run ruff format src tests
	uv run ruff check --fix src tests

# Type check
typecheck:
	uv run mypy src

# Run all checks
check: fmt lint typecheck test
	@echo "All checks passed!"

# Clean build artifacts
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Sync dependencies
sync:
	uv sync

# Upgrade dependencies
upgrade:
	uv lock --upgrade
	uv sync

# Generate OpenAPI schema
openapi:
	uv run python -c "import json; from myapp.main import app; print(json.dumps(app.openapi(), indent=2))" > openapi.json

# Help
help:
	@echo "Available commands:"
	@echo "  dev        - Run development server"
	@echo "  test       - Run tests"
	@echo "  test-cov   - Run tests with coverage"
	@echo "  lint       - Lint code with ruff"
	@echo "  fmt        - Format code with ruff"
	@echo "  typecheck  - Type check with mypy"
	@echo "  check      - Run all checks"
	@echo "  clean      - Clean build artifacts"
	@echo "  sync       - Sync dependencies"
	@echo "  upgrade    - Upgrade dependencies"
	@echo "  openapi    - Generate OpenAPI schema"
