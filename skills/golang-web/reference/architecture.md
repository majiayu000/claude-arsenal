# Architecture Reference

## Table of Contents

1. [Standard Go Project Layout](#standard-go-project-layout)
2. [Layered Architecture](#layered-architecture)
3. [Dependency Injection](#dependency-injection)
4. [Interface Design](#interface-design)
5. [Error Handling](#error-handling)

---

## Standard Go Project Layout

### Overview

```
project/
├── cmd/                       # Main applications
│   └── myapp/
│       └── main.go            # Entry point
├── internal/                  # Private code (not importable)
│   ├── handlers/              # HTTP handlers
│   ├── services/              # Business logic
│   ├── repositories/          # Data access
│   ├── models/                # Domain models
│   ├── middleware/            # HTTP middleware
│   └── router/                # Route setup
├── pkg/                       # Public reusable code
│   ├── errors/
│   ├── logger/
│   ├── response/
│   └── database/
├── configs/                   # Configuration
├── api/                       # OpenAPI/Swagger specs
├── scripts/                   # Build/deploy scripts
├── deployments/               # Docker, K8s configs
└── docs/                      # Documentation
```

### Directory Purposes

| Directory | Purpose | Importable? |
|-----------|---------|-------------|
| `cmd/` | Application entry points | No (main packages) |
| `internal/` | Private application code | No (Go enforced) |
| `pkg/` | Public library code | Yes |
| `configs/` | Configuration loading | Internal use |
| `api/` | API definitions (OpenAPI) | N/A |

### Why internal/?

```go
// internal/ cannot be imported from outside the module
// This is enforced by Go compiler

// ✅ OK: Import within same module
import "github.com/myorg/myapp/internal/services"

// ❌ ERROR: Cannot import from another module
import "github.com/myorg/myapp/internal/services" // Compilation error
```

---

## Layered Architecture

### Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      cmd/main.go                             │
│                   (Dependency Wiring)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    internal/handlers/                        │
│              HTTP Handlers (Gin/Chi/Echo)                    │
│         Parse request → Call service → Return response       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    internal/services/                        │
│                     Business Logic                           │
│        Orchestration, validation, domain rules               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  internal/repositories/                      │
│                     Data Access                              │
│          Database queries, cache operations                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         pkg/                                 │
│                  Shared Infrastructure                       │
│        errors, logger, response, database, cache             │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### Handlers (Presentation)

```go
// internal/handlers/user.go
// Responsibilities:
// - Parse HTTP request
// - Validate input format
// - Call service
// - Format HTTP response
// - NO business logic

func (h *UserHandler) Create(c *gin.Context) {
    // 1. Parse request
    var input CreateUserInput
    if err := c.ShouldBindJSON(&input); err != nil {
        response.Error(c, errors.ErrInvalidParams)
        return
    }

    // 2. Call service (business logic happens there)
    user, err := h.service.Create(c.Request.Context(), input)
    if err != nil {
        response.Error(c, err)
        return
    }

    // 3. Return response
    response.Success(c, user)
}
```

#### Services (Business)

```go
// internal/services/user.go
// Responsibilities:
// - Business rules and validation
// - Orchestrate multiple repositories
// - Transaction management
// - NO HTTP concerns, NO SQL queries

func (s *userService) Create(ctx context.Context, input CreateUserInput) (*models.User, error) {
    // Business rule: Check duplicate
    existing, _ := s.repo.FindByEmail(ctx, input.Email)
    if existing != nil {
        return nil, errors.ErrUserExists
    }

    // Business rule: Hash password
    hashedPassword, err := s.hasher.Hash(input.Password)
    if err != nil {
        return nil, errors.Wrap(err, 500, "failed to hash password")
    }

    user := &models.User{
        ID:       uuid.New().String(),
        Email:    input.Email,
        Password: hashedPassword,
    }

    return s.repo.Save(ctx, user)
}
```

#### Repositories (Data)

```go
// internal/repositories/user.go
// Responsibilities:
// - Database queries
// - Data mapping (DB row → Model)
// - NO business logic

func (r *userRepository) FindByEmail(ctx context.Context, email string) (*models.User, error) {
    var user models.User
    err := r.db.WithContext(ctx).Where("email = ?", email).First(&user).Error
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return nil, nil // Not found is not an error
    }
    return &user, err
}
```

---

## Dependency Injection

### Manual DI in main.go

```go
// cmd/myapp/main.go
func main() {
    cfg := configs.Load()

    // Infrastructure (bottom of dependency graph)
    db := database.New(cfg.Database)
    cache := cache.New(cfg.Redis)
    hasher := security.NewArgon2Hasher()

    // Repositories (depend on infrastructure)
    userRepo := repositories.NewUserRepository(db)
    orderRepo := repositories.NewOrderRepository(db)

    // Services (depend on repositories)
    userService := services.NewUserService(userRepo, hasher)
    orderService := services.NewOrderService(orderRepo, userService)

    // Handlers (depend on services)
    userHandler := handlers.NewUserHandler(userService)
    orderHandler := handlers.NewOrderHandler(orderService)

    // Router (depend on handlers)
    r := router.Setup(userHandler, orderHandler)

    server.Run(r, cfg.Server)
}
```

### Why Manual DI?

| Approach | Pros | Cons |
|----------|------|------|
| Manual DI | Explicit, type-safe, no magic | Verbose for large apps |
| Wire (Google) | Compile-time DI generation | Learning curve |
| Fx (Uber) | Runtime DI, lifecycle management | Runtime errors possible |
| dig (Uber) | Simpler runtime DI | Less type safety |

**Recommendation**: Start with manual DI. Move to Wire only when wiring becomes painful.

---

## Interface Design

### Define Interfaces at Point of Use

```go
// ❌ BAD: Interface defined with implementation
// internal/repositories/user.go
type UserRepository interface { ... }
type userRepository struct { ... }

// ✅ GOOD: Interface defined where it's used
// internal/services/user.go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*models.User, error)
    Save(ctx context.Context, user *models.User) (*models.User, error)
}

type userService struct {
    repo UserRepository // Accepts any implementation
}

// internal/repositories/user.go
type userRepository struct { db *gorm.DB }
// Implicitly implements services.UserRepository
```

### Accept Interfaces, Return Structs

```go
// ✅ GOOD: Accept interface
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// ❌ BAD: Accept concrete type
func NewUserService(repo *PostgresUserRepository) *UserService {
    return &UserService{repo: repo}
}
```

### Keep Interfaces Small

```go
// ❌ BAD: Large interface
type UserRepository interface {
    FindByID(id string) (*User, error)
    FindByEmail(email string) (*User, error)
    FindByPhone(phone string) (*User, error)
    FindAll() ([]*User, error)
    FindByRole(role string) ([]*User, error)
    Save(user *User) (*User, error)
    Update(user *User) error
    Delete(id string) error
    // ... 20 more methods
}

// ✅ GOOD: Small, focused interfaces
type UserFinder interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

type UserSaver interface {
    Save(ctx context.Context, user *User) (*User, error)
}

// Compose when needed
type UserRepository interface {
    UserFinder
    UserSaver
}
```

---

## Error Handling

### Custom Error Types

```go
// pkg/errors/errors.go
type AppError struct {
    Code       int    `json:"code"`
    Message    string `json:"message"`
    HTTPStatus int    `json:"-"`
    Cause      error  `json:"-"`
}

func (e *AppError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Cause)
    }
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Cause
}
```

### Error Wrapping Pattern

```go
// Repository layer: Wrap with context
func (r *userRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
    var user models.User
    if err := r.db.WithContext(ctx).First(&user, "id = ?", id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, nil // Not found is OK
        }
        return nil, errors.Wrap(err, 500, "failed to query user")
    }
    return &user, nil
}

// Service layer: Add business context
func (s *userService) GetByID(ctx context.Context, id string) (*models.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, err // Already wrapped
    }
    if user == nil {
        return nil, errors.ErrNotFound
    }
    return user, nil
}

// Handler layer: Just pass through
func (h *UserHandler) Get(c *gin.Context) {
    user, err := h.service.GetByID(c.Request.Context(), c.Param("id"))
    if err != nil {
        response.Error(c, err) // Error type determines HTTP status
        return
    }
    response.Success(c, user)
}
```

### Error Handling Best Practices

```go
// ✅ DO: Check errors immediately
result, err := doSomething()
if err != nil {
    return nil, err
}

// ✅ DO: Wrap with context
if err != nil {
    return errors.Wrap(err, 500, "failed to process order")
}

// ✅ DO: Use errors.Is for comparison
if errors.Is(err, gorm.ErrRecordNotFound) {
    return nil, nil
}

// ❌ DON'T: Ignore errors
result, _ := doSomething() // Never do this

// ❌ DON'T: Create new error losing context
if err != nil {
    return fmt.Errorf("failed") // Lost original error
}
```
