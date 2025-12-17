.PHONY: build run dev test lint clean tidy upgrade help

APP_NAME=myapp
BUILD_DIR=bin

# Build the application
build:
	@echo "Building $(APP_NAME)..."
	go build -o $(BUILD_DIR)/$(APP_NAME) ./cmd/$(APP_NAME)

# Run the application
run:
	@echo "Running $(APP_NAME)..."
	go run ./cmd/$(APP_NAME)

# Run in development mode with hot reload (requires air)
dev:
	@echo "Running $(APP_NAME) in development mode..."
	air

# Run tests
test:
	@echo "Running tests..."
	go test -v -race ./...

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

# Run linter (requires golangci-lint)
lint:
	@echo "Running linter..."
	golangci-lint run

# Format code
fmt:
	@echo "Formatting code..."
	go fmt ./...

# Run go vet
vet:
	@echo "Running go vet..."
	go vet ./...

# Clean build artifacts
clean:
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR)
	rm -f coverage.out coverage.html

# Tidy dependencies
tidy:
	@echo "Tidying dependencies..."
	go mod tidy

# Upgrade all dependencies to latest
upgrade:
	@echo "Upgrading dependencies..."
	go get -u ./...
	go mod tidy

# Download dependencies
download:
	@echo "Downloading dependencies..."
	go mod download

# Run all checks
check: fmt vet lint test
	@echo "All checks passed!"

# Generate mocks (requires mockery)
mock:
	@echo "Generating mocks..."
	mockery --all

# Help
help:
	@echo "Available commands:"
	@echo "  build         - Build the application"
	@echo "  run           - Run the application"
	@echo "  dev           - Run with hot reload (requires air)"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  lint          - Run linter (requires golangci-lint)"
	@echo "  fmt           - Format code"
	@echo "  vet           - Run go vet"
	@echo "  clean         - Clean build artifacts"
	@echo "  tidy          - Tidy dependencies"
	@echo "  upgrade       - Upgrade all dependencies"
	@echo "  download      - Download dependencies"
	@echo "  check         - Run all checks"
	@echo "  mock          - Generate mocks"
