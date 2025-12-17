# Rust Design Patterns

## Newtype Pattern

Zero-cost wrapper for type safety and encapsulation.

### Basic Usage

```rust
// Type safety: prevent mixing IDs
struct UserId(i64);
struct OrderId(i64);

fn get_user(id: UserId) -> User { ... }
fn get_order(id: OrderId) -> Order { ... }

// Compiler prevents: get_user(order_id)
let user = get_user(UserId(123));
```

### With Validation

```rust
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Email(String);

#[derive(Debug, Error)]
#[error("invalid email: {0}")]
pub struct InvalidEmail(String);

impl Email {
    pub fn new(value: impl Into<String>) -> Result<Self, InvalidEmail> {
        let value = value.into();
        if value.contains('@') && value.contains('.') {
            Ok(Self(value))
        } else {
            Err(InvalidEmail(value))
        }
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Use TryFrom for ergonomic conversion
impl TryFrom<String> for Email {
    type Error = InvalidEmail;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}
```

### With Serde

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(transparent)]
pub struct UserId(i64);

// JSON: just the number, not {"0": 123}
```

### Deref for Convenience

```rust
use std::ops::Deref;

#[derive(Debug, Clone)]
pub struct NonEmptyString(String);

impl Deref for NonEmptyString {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Now you can call str methods directly
let name = NonEmptyString::new("Alice").unwrap();
println!("{}", name.len()); // Works!
```

---

## Builder Pattern

Construct complex objects step by step.

### Basic Builder

```rust
#[derive(Debug)]
pub struct Server {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Duration,
}

#[derive(Default)]
pub struct ServerBuilder {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Duration,
}

impl ServerBuilder {
    pub fn new() -> Self {
        Self {
            host: "127.0.0.1".into(),
            port: 8080,
            max_connections: 100,
            timeout: Duration::from_secs(30),
        }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    pub fn max_connections(mut self, n: usize) -> Self {
        self.max_connections = n;
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn build(self) -> Server {
        Server {
            host: self.host,
            port: self.port,
            max_connections: self.max_connections,
            timeout: self.timeout,
        }
    }
}

// Usage
let server = ServerBuilder::new()
    .host("0.0.0.0")
    .port(3000)
    .max_connections(1000)
    .build();
```

### Builder with Validation

```rust
impl ServerBuilder {
    pub fn build(self) -> Result<Server, BuildError> {
        if self.port == 0 {
            return Err(BuildError::InvalidPort);
        }
        if self.max_connections == 0 {
            return Err(BuildError::InvalidConnections);
        }

        Ok(Server {
            host: self.host,
            port: self.port,
            max_connections: self.max_connections,
            timeout: self.timeout,
        })
    }
}
```

### Mutable Reference Builder

More efficient for reusable builders.

```rust
impl ServerBuilder {
    pub fn host(&mut self, host: impl Into<String>) -> &mut Self {
        self.host = host.into();
        self
    }

    pub fn port(&mut self, port: u16) -> &mut Self {
        self.port = port;
        self
    }

    pub fn build(&self) -> Server {
        Server {
            host: self.host.clone(),
            port: self.port,
            max_connections: self.max_connections,
            timeout: self.timeout,
        }
    }
}

// Usage
let mut builder = ServerBuilder::new();
builder.host("localhost").port(8080);
let server1 = builder.build();
builder.port(9090);
let server2 = builder.build();
```

### derive_builder Crate

```toml
[dependencies]
derive_builder = "*"
```

```rust
use derive_builder::Builder;

#[derive(Builder, Debug)]
#[builder(setter(into))]
pub struct Server {
    host: String,
    #[builder(default = "8080")]
    port: u16,
    #[builder(default = "100")]
    max_connections: usize,
}

// Auto-generated ServerBuilder
let server = ServerBuilder::default()
    .host("localhost")
    .port(3000)
    .build()?;
```

---

## Error Handling Patterns

### Custom Error with thiserror

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("user not found: {id}")]
    UserNotFound { id: i64 },

    #[error("validation failed: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("io error: {0}")]
    Io(#[from] std::io::Error),

    #[error("internal error")]
    Internal(#[source] anyhow::Error),
}

impl AppError {
    pub fn validation(msg: impl Into<String>) -> Self {
        Self::Validation(msg.into())
    }
}
```

### Error Context with anyhow

```rust
use anyhow::{Context, Result, bail, ensure};

fn process_config(path: &Path) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("failed to read config: {}", path.display()))?;

    ensure!(!content.is_empty(), "config file is empty");

    let config: Config = toml::from_str(&content)
        .context("failed to parse config")?;

    if config.port == 0 {
        bail!("port cannot be zero");
    }

    Ok(config)
}
```

### Result Extension Trait

```rust
pub trait ResultExt<T> {
    fn or_not_found(self, resource: &str) -> Result<T, AppError>;
}

impl<T> ResultExt<T> for Option<T> {
    fn or_not_found(self, resource: &str) -> Result<T, AppError> {
        self.ok_or_else(|| AppError::NotFound(resource.into()))
    }
}

// Usage
let user = repo.find_by_id(id).await?.or_not_found("user")?;
```

### Error to HTTP Response (Axum)

```rust
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match &self {
            AppError::UserNotFound { .. } => (StatusCode::NOT_FOUND, self.to_string()),
            AppError::Validation(_) => (StatusCode::BAD_REQUEST, self.to_string()),
            AppError::Database(_) | AppError::Internal(_) => {
                tracing::error!(?self, "internal error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into())
            }
            AppError::Io(_) => (StatusCode::INTERNAL_SERVER_ERROR, "io error".into()),
        };

        (status, Json(serde_json::json!({ "error": message }))).into_response()
    }
}
```

---

## Repository Pattern

Abstract data access behind traits.

```rust
use async_trait::async_trait;

// Domain model
#[derive(Debug, Clone)]
pub struct User {
    pub id: UserId,
    pub email: Email,
    pub name: String,
}

// Repository trait (defined in domain layer)
#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>>;
    async fn find_by_email(&self, email: &Email) -> Result<Option<User>>;
    async fn save(&self, user: &User) -> Result<()>;
    async fn delete(&self, id: UserId) -> Result<()>;
}

// SQLx implementation
pub struct PgUserRepository {
    pool: PgPool,
}

impl PgUserRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl UserRepository for PgUserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>> {
        let row = sqlx::query_as!(
            UserRow,
            "SELECT id, email, name FROM users WHERE id = $1",
            id.0
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(row.map(User::from))
    }

    // ... other methods
}
```

### In-Memory Implementation (Testing)

```rust
use std::collections::HashMap;
use std::sync::RwLock;

pub struct InMemoryUserRepository {
    users: RwLock<HashMap<UserId, User>>,
}

impl InMemoryUserRepository {
    pub fn new() -> Self {
        Self {
            users: RwLock::new(HashMap::new()),
        }
    }
}

#[async_trait]
impl UserRepository for InMemoryUserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>> {
        Ok(self.users.read().unwrap().get(&id).cloned())
    }

    async fn save(&self, user: &User) -> Result<()> {
        self.users.write().unwrap().insert(user.id.clone(), user.clone());
        Ok(())
    }

    // ...
}
```

---

## Service Pattern

Business logic with injected dependencies.

```rust
pub struct UserService<R: UserRepository> {
    repo: R,
}

impl<R: UserRepository> UserService<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    pub async fn create(&self, input: CreateUserInput) -> Result<User> {
        // Validate
        let email = Email::new(&input.email)?;

        // Check uniqueness
        if self.repo.find_by_email(&email).await?.is_some() {
            return Err(AppError::validation("email already exists"));
        }

        // Create
        let user = User {
            id: UserId::new(),
            email,
            name: input.name,
        };

        self.repo.save(&user).await?;
        Ok(user)
    }

    pub async fn get(&self, id: UserId) -> Result<User> {
        self.repo
            .find_by_id(id)
            .await?
            .ok_or(AppError::UserNotFound { id: id.0 })
    }
}
```

### With Arc for Shared State

```rust
use std::sync::Arc;

pub struct AppState {
    pub user_service: UserService<PgUserRepository>,
}

impl AppState {
    pub fn new(pool: PgPool) -> Arc<Self> {
        let repo = PgUserRepository::new(pool);
        Arc::new(Self {
            user_service: UserService::new(repo),
        })
    }
}

// In Axum
let state = AppState::new(pool);
let app = Router::new()
    .route("/users", post(create_user))
    .with_state(state);

async fn create_user(
    State(state): State<Arc<AppState>>,
    Json(input): Json<CreateUserInput>,
) -> Result<Json<User>, AppError> {
    let user = state.user_service.create(input).await?;
    Ok(Json(user))
}
```

---

## Type State Pattern

Compile-time state machine.

```rust
// States (zero-sized types)
pub struct Draft;
pub struct Published;
pub struct Archived;

// Document with state parameter
pub struct Document<State> {
    id: i64,
    title: String,
    content: String,
    _state: std::marker::PhantomData<State>,
}

impl Document<Draft> {
    pub fn new(title: String, content: String) -> Self {
        Self {
            id: 0,
            title,
            content,
            _state: std::marker::PhantomData,
        }
    }

    pub fn edit(&mut self, content: String) {
        self.content = content;
    }

    pub fn publish(self) -> Document<Published> {
        Document {
            id: self.id,
            title: self.title,
            content: self.content,
            _state: std::marker::PhantomData,
        }
    }
}

impl Document<Published> {
    // Can't edit published documents!

    pub fn archive(self) -> Document<Archived> {
        Document {
            id: self.id,
            title: self.title,
            content: self.content,
            _state: std::marker::PhantomData,
        }
    }
}

// Usage
let mut doc = Document::<Draft>::new("Title".into(), "Content".into());
doc.edit("New content".into());  // OK
let published = doc.publish();
// published.edit(...);  // Compile error!
let archived = published.archive();
```

---

## Extension Trait Pattern

Add methods to foreign types.

```rust
pub trait StringExt {
    fn truncate_with_ellipsis(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn truncate_with_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len.saturating_sub(3)])
        }
    }
}

// Usage
let title = "Very long title here".truncate_with_ellipsis(10);
```

### For Option/Result

```rust
pub trait OptionExt<T> {
    fn ok_or_not_found(self, msg: &str) -> Result<T, AppError>;
}

impl<T> OptionExt<T> for Option<T> {
    fn ok_or_not_found(self, msg: &str) -> Result<T, AppError> {
        self.ok_or_else(|| AppError::NotFound(msg.into()))
    }
}

// Usage
let user = repo.find(id).await?.ok_or_not_found("user")?;
```

---

## From/Into Conversion

```rust
// Domain model
pub struct User {
    pub id: UserId,
    pub email: Email,
    pub name: String,
}

// Database row
struct UserRow {
    id: i64,
    email: String,
    name: String,
}

// API response
#[derive(Serialize)]
struct UserResponse {
    id: i64,
    email: String,
    name: String,
}

impl From<UserRow> for User {
    fn from(row: UserRow) -> Self {
        Self {
            id: UserId(row.id),
            email: Email::new_unchecked(row.email), // Trust DB data
            name: row.name,
        }
    }
}

impl From<User> for UserResponse {
    fn from(user: User) -> Self {
        Self {
            id: user.id.0,
            email: user.email.into_string(),
            name: user.name,
        }
    }
}

// Usage
let user: User = row.into();
let response: UserResponse = user.into();
```

---

## Summary Table

| Pattern | Use Case |
|---------|----------|
| Newtype | Type safety, validation, encapsulation |
| Builder | Complex object construction |
| Repository | Abstract data access |
| Service | Business logic with DI |
| Type State | Compile-time state machines |
| Extension Trait | Add methods to foreign types |
| From/Into | Type conversions |
