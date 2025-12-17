# Go Design Patterns Reference

## Table of Contents

1. [Repository Pattern](#repository-pattern)
2. [Service Pattern](#service-pattern)
3. [Functional Options](#functional-options)
4. [Middleware Pattern](#middleware-pattern)
5. [Graceful Shutdown](#graceful-shutdown)
6. [Context Usage](#context-usage)

---

## Repository Pattern

Abstract data access behind interfaces:

```go
// internal/repositories/user.go

// Interface - defined where it's USED (in services)
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*models.User, error)
    FindByEmail(ctx context.Context, email string) (*models.User, error)
    Save(ctx context.Context, user *models.User) (*models.User, error)
    Delete(ctx context.Context, id string) error
}

// Implementation
type userRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *userRepository {
    return &userRepository{db: db}
}

func (r *userRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
    var user models.User
    if err := r.db.WithContext(ctx).First(&user, "id = ?", id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, nil
        }
        return nil, err
    }
    return &user, nil
}

func (r *userRepository) Save(ctx context.Context, user *models.User) (*models.User, error) {
    if err := r.db.WithContext(ctx).Save(user).Error; err != nil {
        return nil, err
    }
    return user, nil
}
```

### In-Memory Repository for Testing

```go
// internal/repositories/user_memory.go
type inMemoryUserRepository struct {
    users map[string]*models.User
    mu    sync.RWMutex
}

func NewInMemoryUserRepository() *inMemoryUserRepository {
    return &inMemoryUserRepository{
        users: make(map[string]*models.User),
    }
}

func (r *inMemoryUserRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    user, ok := r.users[id]
    if !ok {
        return nil, nil
    }
    return user, nil
}

func (r *inMemoryUserRepository) Save(ctx context.Context, user *models.User) (*models.User, error) {
    r.mu.Lock()
    defer r.mu.Unlock()
    r.users[user.ID] = user
    return user, nil
}
```

---

## Service Pattern

Encapsulate business logic:

```go
// internal/services/user.go

type UserService interface {
    Create(ctx context.Context, input CreateUserInput) (*models.User, error)
    GetByID(ctx context.Context, id string) (*models.User, error)
    Update(ctx context.Context, id string, input UpdateUserInput) (*models.User, error)
    Delete(ctx context.Context, id string) error
}

type userService struct {
    repo   UserRepository
    hasher PasswordHasher
    events EventPublisher
}

func NewUserService(repo UserRepository, hasher PasswordHasher, events EventPublisher) UserService {
    return &userService{
        repo:   repo,
        hasher: hasher,
        events: events,
    }
}

func (s *userService) Create(ctx context.Context, input CreateUserInput) (*models.User, error) {
    // Business rule: Check duplicate email
    existing, err := s.repo.FindByEmail(ctx, input.Email)
    if err != nil {
        return nil, errors.Wrap(err, 500, "failed to check email")
    }
    if existing != nil {
        return nil, errors.ErrUserExists
    }

    // Business rule: Hash password
    hashedPassword, err := s.hasher.Hash(input.Password)
    if err != nil {
        return nil, errors.Wrap(err, 500, "failed to hash password")
    }

    user := &models.User{
        ID:        uuid.New().String(),
        Email:     input.Email,
        Password:  hashedPassword,
        CreatedAt: time.Now(),
    }

    saved, err := s.repo.Save(ctx, user)
    if err != nil {
        return nil, errors.Wrap(err, 500, "failed to save user")
    }

    // Publish event (async)
    s.events.Publish("user.created", UserCreatedEvent{UserID: saved.ID})

    return saved, nil
}
```

---

## Functional Options

Configure structs with optional parameters:

```go
// pkg/server/server.go

type Server struct {
    port         int
    readTimeout  time.Duration
    writeTimeout time.Duration
    handler      http.Handler
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) {
        s.port = port
    }
}

func WithReadTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.readTimeout = d
    }
}

func WithWriteTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.writeTimeout = d
    }
}

func NewServer(handler http.Handler, opts ...Option) *Server {
    // Defaults
    s := &Server{
        port:         8080,
        readTimeout:  30 * time.Second,
        writeTimeout: 30 * time.Second,
        handler:      handler,
    }

    // Apply options
    for _, opt := range opts {
        opt(s)
    }

    return s
}

// Usage
server := NewServer(handler,
    WithPort(9090),
    WithReadTimeout(60*time.Second),
)
```

### Builder Alternative

```go
type ServerBuilder struct {
    server *Server
}

func NewServerBuilder(handler http.Handler) *ServerBuilder {
    return &ServerBuilder{
        server: &Server{
            port:    8080,
            handler: handler,
        },
    }
}

func (b *ServerBuilder) Port(p int) *ServerBuilder {
    b.server.port = p
    return b
}

func (b *ServerBuilder) ReadTimeout(d time.Duration) *ServerBuilder {
    b.server.readTimeout = d
    return b
}

func (b *ServerBuilder) Build() *Server {
    return b.server
}

// Usage
server := NewServerBuilder(handler).
    Port(9090).
    ReadTimeout(60 * time.Second).
    Build()
```

---

## Middleware Pattern

Chain HTTP handlers:

```go
// internal/middleware/middleware.go

// Middleware type
type Middleware func(http.Handler) http.Handler

// Chain combines multiple middleware
func Chain(middlewares ...Middleware) Middleware {
    return func(next http.Handler) http.Handler {
        for i := len(middlewares) - 1; i >= 0; i-- {
            next = middlewares[i](next)
        }
        return next
    }
}

// Logger middleware
func Logger(logger *slog.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // Wrap response writer to capture status
            ww := &responseWriter{ResponseWriter: w, status: 200}

            next.ServeHTTP(ww, r)

            logger.Info("http request",
                "method", r.Method,
                "path", r.URL.Path,
                "status", ww.status,
                "duration", time.Since(start),
            )
        })
    }
}

// Recovery middleware
func Recovery() Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if err := recover(); err != nil {
                    w.WriteHeader(http.StatusInternalServerError)
                    slog.Error("panic recovered", "error", err)
                }
            }()
            next.ServeHTTP(w, r)
        })
    }
}

// RequestID middleware
func RequestID() Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            requestID := r.Header.Get("X-Request-ID")
            if requestID == "" {
                requestID = uuid.New().String()
            }

            ctx := context.WithValue(r.Context(), "request_id", requestID)
            w.Header().Set("X-Request-ID", requestID)

            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// Usage
handler := Chain(
    Recovery(),
    RequestID(),
    Logger(logger),
)(router)
```

### Gin Middleware

```go
// internal/middleware/gin.go

func GinLogger(logger *slog.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()

        c.Next()

        logger.Info("http request",
            "method", c.Request.Method,
            "path", c.Request.URL.Path,
            "status", c.Writer.Status(),
            "duration", time.Since(start),
            "client_ip", c.ClientIP(),
        )
    }
}

func GinRecovery() gin.HandlerFunc {
    return func(c *gin.Context) {
        defer func() {
            if err := recover(); err != nil {
                slog.Error("panic recovered", "error", err)
                c.AbortWithStatus(http.StatusInternalServerError)
            }
        }()
        c.Next()
    }
}
```

---

## Graceful Shutdown

Handle shutdown signals properly:

```go
// pkg/server/server.go

func (s *Server) Run() error {
    srv := &http.Server{
        Addr:         fmt.Sprintf(":%d", s.port),
        Handler:      s.handler,
        ReadTimeout:  s.readTimeout,
        WriteTimeout: s.writeTimeout,
    }

    // Channel to listen for errors from ListenAndServe
    errChan := make(chan error, 1)

    go func() {
        slog.Info("server starting", "port", s.port)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            errChan <- err
        }
    }()

    // Channel to listen for OS signals
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // Block until signal or error
    select {
    case err := <-errChan:
        return fmt.Errorf("server error: %w", err)
    case sig := <-quit:
        slog.Info("shutdown signal received", "signal", sig)
    }

    // Graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        return fmt.Errorf("server shutdown error: %w", err)
    }

    slog.Info("server stopped gracefully")
    return nil
}
```

### With Cleanup Functions

```go
// pkg/server/server.go

type CleanupFunc func(context.Context) error

func (s *Server) RunWithCleanup(cleanups ...CleanupFunc) error {
    // ... server start code ...

    // After shutdown signal
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    // Shutdown HTTP server
    if err := srv.Shutdown(ctx); err != nil {
        slog.Error("server shutdown error", "error", err)
    }

    // Run cleanup functions
    for _, cleanup := range cleanups {
        if err := cleanup(ctx); err != nil {
            slog.Error("cleanup error", "error", err)
        }
    }

    return nil
}

// Usage
server.RunWithCleanup(
    db.Close,
    cache.Close,
    eventBus.Close,
)
```

---

## Context Usage

Pass context through the call chain:

```go
// ✅ GOOD: Context as first parameter
func (s *userService) GetByID(ctx context.Context, id string) (*models.User, error) {
    return s.repo.FindByID(ctx, id)
}

// ✅ GOOD: Extract values from context
func GetRequestID(ctx context.Context) string {
    if id, ok := ctx.Value("request_id").(string); ok {
        return id
    }
    return ""
}

// ✅ GOOD: Use context for cancellation
func (s *userService) LongOperation(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            // Do work
        }
    }
}

// ❌ BAD: Context not first parameter
func BadFunc(id string, ctx context.Context) error { ... }

// ❌ BAD: Storing context in struct
type BadService struct {
    ctx context.Context // Never do this
}

// ❌ BAD: Using context.Background() in handlers
func (h *Handler) Get(c *gin.Context) {
    user, _ := h.service.GetByID(context.Background(), id) // Use c.Request.Context()
}
```

### Context Keys

```go
// pkg/ctxkeys/keys.go

type contextKey string

const (
    RequestIDKey contextKey = "request_id"
    UserIDKey    contextKey = "user_id"
    TraceIDKey   contextKey = "trace_id"
)

func WithRequestID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, RequestIDKey, id)
}

func RequestID(ctx context.Context) string {
    if id, ok := ctx.Value(RequestIDKey).(string); ok {
        return id
    }
    return ""
}
```
