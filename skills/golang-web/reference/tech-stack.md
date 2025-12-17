# Tech Stack Reference

## Table of Contents

1. [Version Strategy](#version-strategy)
2. [HTTP Framework](#http-framework)
3. [Configuration](#configuration)
4. [Logging](#logging)
5. [Database](#database)
6. [Validation](#validation)
7. [Testing](#testing)
8. [Linting](#linting)
9. [Decision Matrix](#decision-matrix)

---

## Version Strategy

> **Always use latest. `go.mod` handles version locking.**

### Why No Pinned Versions

- Go modules automatically track versions in `go.mod`
- `go.sum` ensures reproducible builds
- `go get -u` updates to latest compatible version

### How to Stay Current

```bash
# Update all dependencies
go get -u ./...
go mod tidy

# Update specific package
go get -u github.com/gin-gonic/gin

# Check for available updates
go list -m -u all

# Verify dependencies
go mod verify
```

### Package Installation

```bash
# Always install without version
go get github.com/gin-gonic/gin      # Gets latest
go get github.com/spf13/viper        # Gets latest

# Never do this in templates
go get github.com/gin-gonic/gin@v1.9.0  # Pinned = outdated
```

---

## HTTP Framework

### Gin (Recommended)

```bash
go get github.com/gin-gonic/gin
```

```go
import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()

    r.GET("/users/:id", getUser)
    r.POST("/users", createUser)

    r.Run(":8080")
}
```

**Pros:**
- Most popular, largest ecosystem
- Fast (uses httprouter)
- Good middleware support
- Excellent documentation

### Chi (Lightweight alternative)

```bash
go get github.com/go-chi/chi/v5
```

```go
import "github.com/go-chi/chi/v5"

func main() {
    r := chi.NewRouter()
    r.Use(middleware.Logger)

    r.Get("/users/{id}", getUser)
    r.Post("/users", createUser)

    http.ListenAndServe(":8080", r)
}
```

**Pros:**
- Lightweight, stdlib compatible
- Composable middleware
- No external dependencies

### Echo (Feature-rich)

```bash
go get github.com/labstack/echo/v4
```

```go
import "github.com/labstack/echo/v4"

func main() {
    e := echo.New()

    e.GET("/users/:id", getUser)
    e.POST("/users", createUser)

    e.Start(":8080")
}
```

**Pros:**
- Built-in features (validation, binding)
- Good performance
- Clean API

### Comparison

| Framework | Performance | Ecosystem | Learning Curve | stdlib Compatible |
|-----------|-------------|-----------|----------------|-------------------|
| Gin | Excellent | Large | Low | No |
| Chi | Excellent | Medium | Low | Yes |
| Echo | Excellent | Medium | Low | No |
| Fiber | Fastest | Growing | Low | No |
| stdlib | Good | N/A | Medium | Yes |

---

## Configuration

### Viper (Recommended)

```bash
go get github.com/spf13/viper
```

```go
import "github.com/spf13/viper"

type Config struct {
    Server struct {
        Port int    `mapstructure:"port"`
        Mode string `mapstructure:"mode"`
    } `mapstructure:"server"`
    Database struct {
        Host     string `mapstructure:"host"`
        Port     int    `mapstructure:"port"`
        Password string `mapstructure:"password"`
    } `mapstructure:"database"`
}

func Load() *Config {
    viper.SetConfigFile("config.yaml")
    viper.AutomaticEnv()
    viper.SetEnvPrefix("APP")
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    // Defaults
    viper.SetDefault("server.port", 8080)

    viper.ReadInConfig()

    var cfg Config
    viper.Unmarshal(&cfg)
    return &cfg
}
```

**Features:**
- YAML, JSON, TOML, ENV support
- Environment variable override
- Default values
- Live config reload

### Envconfig (Simpler)

```bash
go get github.com/kelseyhightower/envconfig
```

```go
import "github.com/kelseyhightower/envconfig"

type Config struct {
    Port     int    `envconfig:"PORT" default:"8080"`
    DBHost   string `envconfig:"DB_HOST" required:"true"`
    LogLevel string `envconfig:"LOG_LEVEL" default:"info"`
}

func Load() *Config {
    var cfg Config
    envconfig.Process("APP", &cfg)
    return &cfg
}
```

**Pros:** Simple, environment-variable focused

---

## Logging

### Slog (Go 1.21+ stdlib)

```go
import "log/slog"

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))
    slog.SetDefault(logger)

    slog.Info("server started", "port", 8080)
    slog.Error("failed to connect", "error", err)
}
```

**Pros:** Stdlib, structured, no dependencies

### Logrus (Battle-tested)

```bash
go get github.com/sirupsen/logrus
```

```go
import "github.com/sirupsen/logrus"

var log = logrus.New()

func init() {
    log.SetFormatter(&logrus.JSONFormatter{})
    log.SetLevel(logrus.InfoLevel)
}

func main() {
    log.WithFields(logrus.Fields{
        "port": 8080,
    }).Info("server started")
}
```

**Pros:** Popular, feature-rich, hooks support

### Zap (Performance)

```bash
go get go.uber.org/zap
```

```go
import "go.uber.org/zap"

func main() {
    logger, _ := zap.NewProduction()
    defer logger.Sync()

    logger.Info("server started",
        zap.Int("port", 8080),
    )
}
```

**Pros:** Fastest, zero-allocation

### Comparison

| Library | Performance | Ease of Use | Stdlib |
|---------|-------------|-------------|--------|
| slog | Good | Easy | Yes |
| Logrus | Medium | Easy | No |
| Zap | Excellent | Medium | No |
| Zerolog | Excellent | Easy | No |

---

## Database

### GORM (Full ORM)

```bash
go get gorm.io/gorm
go get gorm.io/driver/postgres
```

```go
import (
    "gorm.io/gorm"
    "gorm.io/driver/postgres"
)

type User struct {
    ID    string `gorm:"primaryKey"`
    Email string `gorm:"uniqueIndex"`
    Name  string
}

func main() {
    db, _ := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    db.AutoMigrate(&User{})

    // Create
    db.Create(&User{ID: "1", Email: "test@test.com"})

    // Query
    var user User
    db.First(&user, "email = ?", "test@test.com")
}
```

**Pros:** Feature-rich, migrations, associations

### sqlx (SQL + Struct mapping)

```bash
go get github.com/jmoiron/sqlx
```

```go
import "github.com/jmoiron/sqlx"

type User struct {
    ID    string `db:"id"`
    Email string `db:"email"`
}

func main() {
    db := sqlx.MustConnect("postgres", dsn)

    var user User
    db.Get(&user, "SELECT * FROM users WHERE id = $1", "1")

    var users []User
    db.Select(&users, "SELECT * FROM users WHERE active = $1", true)
}
```

**Pros:** Direct SQL control, good performance

### sqlc (Compile-time type-safe SQL)

```bash
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
```

```sql
-- query.sql
-- name: GetUser :one
SELECT * FROM users WHERE id = $1;

-- name: CreateUser :one
INSERT INTO users (id, email) VALUES ($1, $2) RETURNING *;
```

```go
// Generated code
func (q *Queries) GetUser(ctx context.Context, id string) (User, error)
func (q *Queries) CreateUser(ctx context.Context, arg CreateUserParams) (User, error)
```

**Pros:** Type-safe SQL, compile-time checks

### Comparison

| Library | Type Safety | Performance | Learning Curve |
|---------|-------------|-------------|----------------|
| GORM | Good | Medium | Low |
| sqlx | Medium | Good | Low |
| sqlc | Excellent | Excellent | Medium |
| Ent | Excellent | Good | High |

---

## Validation

### go-playground/validator

```bash
go get github.com/go-playground/validator/v10
```

```go
import "github.com/go-playground/validator/v10"

type CreateUserInput struct {
    Email    string `json:"email" validate:"required,email"`
    Password string `json:"password" validate:"required,min=8"`
    Age      int    `json:"age" validate:"gte=0,lte=120"`
}

var validate = validator.New()

func ValidateStruct(s interface{}) error {
    return validate.Struct(s)
}
```

**Pros:** Standard choice, many validators, custom rules

### ozzo-validation

```bash
go get github.com/go-ozzo/ozzo-validation/v4
```

```go
import validation "github.com/go-ozzo/ozzo-validation/v4"

type CreateUserInput struct {
    Email    string
    Password string
}

func (i CreateUserInput) Validate() error {
    return validation.ValidateStruct(&i,
        validation.Field(&i.Email, validation.Required, is.Email),
        validation.Field(&i.Password, validation.Required, validation.Length(8, 100)),
    )
}
```

**Pros:** Fluent API, validation in structs

---

## Testing

### testify (Recommended)

```bash
go get github.com/stretchr/testify
```

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"
)

func TestUserService_Create(t *testing.T) {
    // Arrange
    repo := NewMockUserRepository()
    service := NewUserService(repo)

    // Act
    user, err := service.Create(ctx, input)

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "test@test.com", user.Email)
}

// Table-driven tests
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "test@test.com", false},
        {"invalid email", "invalid", true},
        {"empty email", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### mockery (Mock generation)

```bash
go install github.com/vektra/mockery/v2@latest
```

```go
//go:generate mockery --name=UserRepository
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

// Generated mock in mocks/UserRepository.go
```

---

## Linting

### golangci-lint (Recommended)

```bash
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

```yaml
# .golangci.yml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports
    - misspell

linters-settings:
  errcheck:
    check-type-assertions: true
  govet:
    check-shadowing: true
```

```bash
golangci-lint run
```

---

## Decision Matrix

### For New Projects

| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| HTTP | Gin | Chi |
| Config | Viper | Envconfig |
| Logging | slog (stdlib) | Logrus |
| Database | GORM | sqlx / sqlc |
| Validation | validator | ozzo-validation |
| Testing | testify | stdlib |
| Linting | golangci-lint | - |

### Stack Combinations

**Feature-rich stack:**
```
Gin + Viper + Logrus + GORM + validator + testify
```

**Lightweight stack:**
```
Chi + Envconfig + slog + sqlx + validator + stdlib testing
```

**Type-safe stack:**
```
Chi + Viper + slog + sqlc + validator + testify
```
