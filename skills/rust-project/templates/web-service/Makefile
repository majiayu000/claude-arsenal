.PHONY: build run dev test lint fmt check clean db-create db-migrate db-prepare

APP_NAME = myapp

# Build release binary
build:
	cargo build --release

# Run in development mode
run:
	cargo run

# Run with auto-reload (requires cargo-watch)
dev:
	cargo watch -x run

# Run tests
test:
	cargo test

# Run tests with coverage (requires cargo-tarpaulin)
test-coverage:
	cargo tarpaulin --out Html

# Run clippy linter
lint:
	cargo clippy -- -D warnings

# Format code
fmt:
	cargo fmt

# Check formatting without modifying
fmt-check:
	cargo fmt --check

# Run all checks
check: fmt lint test
	@echo "All checks passed!"

# Clean build artifacts
clean:
	cargo clean

# Update dependencies
upgrade:
	cargo update

# Database commands (requires sqlx-cli)
db-create:
	sqlx database create

db-drop:
	sqlx database drop

db-migrate:
	sqlx migrate run

db-revert:
	sqlx migrate revert

# Prepare SQLx offline mode
db-prepare:
	cargo sqlx prepare

# Help
help:
	@echo "Available commands:"
	@echo "  build        - Build release binary"
	@echo "  run          - Run in development mode"
	@echo "  dev          - Run with auto-reload"
	@echo "  test         - Run tests"
	@echo "  lint         - Run clippy linter"
	@echo "  fmt          - Format code"
	@echo "  check        - Run all checks"
	@echo "  clean        - Clean build artifacts"
	@echo "  db-create    - Create database"
	@echo "  db-migrate   - Run migrations"
	@echo "  db-prepare   - Prepare SQLx offline mode"
