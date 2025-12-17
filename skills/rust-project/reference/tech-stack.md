# Rust Tech Stack

## Version Strategy

> **Always use latest. Never pin versions in templates.**

```toml
[dependencies]
tokio = { version = "*", features = ["full"] }
axum = "*"
serde = { version = "*", features = ["derive"] }
```

- `cargo update` fetches latest compatible versions
- `Cargo.lock` ensures reproducible builds
- Breaking changes are handled by reading changelogs
- For libraries: use semver ranges (`"1"` or `">=1.0, <2"`)

---

## Async Runtime

### Tokio (Recommended)

The de facto standard for async Rust. Powers Axum, SQLx, reqwest.

```toml
[dependencies]
tokio = { version = "*", features = ["full"] }
# Or minimal:
tokio = { version = "*", features = ["rt-multi-thread", "macros"] }
```

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // Background task
    });
    handle.await.unwrap();
}
```

### async-std

Alternative runtime, slightly different API.

```toml
[dependencies]
async-std = { version = "*", features = ["attributes"] }
```

**When to choose:**
- **Tokio**: Most ecosystem support, production proven
- **async-std**: Simpler API, closer to std

---

## Web Frameworks

### Axum (Recommended)

Built by Tokio team. Ergonomic, Tower middleware, type-safe extractors.

```toml
[dependencies]
axum = "*"
tower = "*"
tower-http = { version = "*", features = ["cors", "trace"] }
```

```rust
use axum::{Router, routing::get, extract::State};

async fn handler(State(db): State<PgPool>) -> impl IntoResponse {
    Json(json!({ "status": "ok" }))
}

let app = Router::new()
    .route("/health", get(handler))
    .with_state(db);
```

### Actix Web

Highest raw performance, actor model.

```toml
[dependencies]
actix-web = "*"
```

```rust
use actix_web::{web, App, HttpServer, Responder};

async fn handler() -> impl Responder {
    web::Json(json!({ "status": "ok" }))
}

HttpServer::new(|| App::new().route("/", web::get().to(handler)))
    .bind("127.0.0.1:8080")?
    .run()
    .await
```

### Rocket

Convention over configuration, most ergonomic.

```toml
[dependencies]
rocket = "*"
```

### Comparison

| Feature | Axum | Actix Web | Rocket |
|---------|------|-----------|--------|
| Performance | Excellent | Best | Good |
| Ergonomics | Great | Good | Best |
| Tokio integration | Native | Custom runtime | Tokio |
| Middleware | Tower | Actix | Fairings |
| Learning curve | Medium | Steep | Easy |
| Production use | Growing | Mature | Mature |

**Recommendation**: Axum for new projects (best balance).

---

## Database

### SQLx (Recommended)

Compile-time checked SQL, async, pure Rust.

```toml
[dependencies]
sqlx = { version = "*", features = ["runtime-tokio", "tls-native-tls", "postgres", "macros", "migrate"] }
```

```rust
// Compile-time verified query
let user = sqlx::query_as!(
    User,
    "SELECT id, name, email FROM users WHERE id = $1",
    id
)
.fetch_one(&pool)
.await?;

// Dynamic query
let users = sqlx::query("SELECT * FROM users WHERE active = $1")
    .bind(true)
    .fetch_all(&pool)
    .await?;
```

**Key features:**
- Compile-time SQL verification
- No DSL, just SQL
- Async-first design
- Automatic migrations

### Diesel

Type-safe DSL, synchronous (async via diesel-async).

```toml
[dependencies]
diesel = { version = "*", features = ["postgres"] }
```

```rust
use diesel::prelude::*;

users::table
    .filter(users::active.eq(true))
    .load::<User>(&mut conn)?
```

### SeaORM

ActiveRecord-style, async, dynamic queries.

```toml
[dependencies]
sea-orm = { version = "*", features = ["runtime-tokio-native-tls", "sqlx-postgres"] }
```

### Comparison

| Feature | SQLx | Diesel | SeaORM |
|---------|------|--------|--------|
| Query style | Raw SQL | DSL | ActiveRecord |
| Compile-time check | SQL verified | Type-safe DSL | Runtime |
| Async | Native | diesel-async | Native |
| Migrations | Built-in | diesel_migrations | Built-in |
| Learning curve | Easy | Medium | Easy |

**Recommendation**: SQLx for compile-time safety with raw SQL control.

---

## CLI Parsing

### Clap (Recommended)

Most feature-complete, derive macros.

```toml
[dependencies]
clap = { version = "*", features = ["derive"] }
```

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    /// Input file
    #[arg(short, long)]
    input: PathBuf,

    /// Verbosity level
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,

    #[command(subcommand)]
    command: Commands,
}

#[derive(clap::Subcommand)]
enum Commands {
    /// Process files
    Process { files: Vec<PathBuf> },
    /// Show config
    Config,
}
```

### argh

Google's lightweight alternative.

```toml
[dependencies]
argh = "*"
```

**Recommendation**: Clap for full-featured CLI, argh for simplicity.

---

## Error Handling

### thiserror (Libraries)

Derive macros for custom error types.

```toml
[dependencies]
thiserror = "*"
```

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum MyError {
    #[error("not found: {0}")]
    NotFound(String),

    #[error("invalid input: {message}")]
    Validation { message: String },

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("io error")]
    Io(#[from] std::io::Error),
}
```

### anyhow (Applications)

Convenient error handling for apps.

```toml
[dependencies]
anyhow = "*"
```

```rust
use anyhow::{Context, Result, bail};

fn process_file(path: &Path) -> Result<Data> {
    let content = std::fs::read_to_string(path)
        .context("failed to read input file")?;

    if content.is_empty() {
        bail!("file is empty");
    }

    Ok(parse(content)?)
}
```

### eyre

anyhow alternative with better error reports.

```toml
[dependencies]
eyre = "*"
color-eyre = "*"  # Pretty error reports
```

### Comparison

| Crate | Use Case | Features |
|-------|----------|----------|
| thiserror | Libraries | Custom error types, From impls |
| anyhow | Applications | Easy error handling, context |
| eyre | Applications | Better reports, custom hooks |
| snafu | Large projects | Context selectors, backtraces |

**Recommendation**: thiserror for libs, anyhow for apps.

---

## Serialization

### Serde (Required)

The serialization framework for Rust.

```toml
[dependencies]
serde = { version = "*", features = ["derive"] }
serde_json = "*"
```

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    id: i64,
    full_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    email: Option<String>,
    #[serde(default)]
    active: bool,
}
```

### Format Crates

```toml
[dependencies]
serde_json = "*"        # JSON
toml = "*"              # TOML (config files)
serde_yaml = "*"        # YAML
csv = "*"               # CSV
```

---

## Logging & Tracing

### tracing (Recommended)

Structured diagnostics, async-aware.

```toml
[dependencies]
tracing = "*"
tracing-subscriber = { version = "*", features = ["env-filter"] }
```

```rust
use tracing::{info, warn, error, instrument, span, Level};

// Initialize
tracing_subscriber::fmt()
    .with_env_filter("myapp=debug,tower_http=debug")
    .init();

// Logging
info!(user_id = %id, "user logged in");
warn!(?error, "operation failed, retrying");

// Instrument functions
#[instrument(skip(db))]
async fn get_user(db: &PgPool, id: i64) -> Result<User> {
    info!("fetching user");
    // ...
}

// Manual spans
let span = span!(Level::INFO, "processing", batch_size = items.len());
let _guard = span.enter();
```

### log (Legacy)

Simple logging facade.

```toml
[dependencies]
log = "*"
env_logger = "*"
```

**Recommendation**: tracing for new projects (async-aware, structured).

---

## HTTP Client

### reqwest (Recommended)

High-level async HTTP client.

```toml
[dependencies]
reqwest = { version = "*", features = ["json"] }
```

```rust
let client = reqwest::Client::new();

let response = client
    .post("https://api.example.com/users")
    .json(&user)
    .send()
    .await?
    .json::<ApiResponse>()
    .await?;
```

### ureq

Blocking HTTP client, minimal dependencies.

```toml
[dependencies]
ureq = { version = "*", features = ["json"] }
```

**Recommendation**: reqwest for async, ureq for sync/simple scripts.

---

## Configuration

### config-rs (Recommended)

Layered configuration from multiple sources.

```toml
[dependencies]
config = "*"
```

```rust
use config::{Config, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Settings {
    server: ServerConfig,
    database: DatabaseConfig,
}

fn load_config() -> Result<Settings, config::ConfigError> {
    Config::builder()
        .add_source(File::with_name("config/default"))
        .add_source(File::with_name("config/local").required(false))
        .add_source(Environment::with_prefix("APP").separator("__"))
        .build()?
        .try_deserialize()
}
```

### figment

Alternative with better composition.

```toml
[dependencies]
figment = { version = "*", features = ["toml", "env"] }
```

---

## Testing

### Built-in + tokio-test

```toml
[dev-dependencies]
tokio-test = "*"
```

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sync() {
        assert_eq!(add(2, 2), 4);
    }

    #[tokio::test]
    async fn test_async() {
        let result = async_operation().await;
        assert!(result.is_ok());
    }
}
```

### Test Utilities

```toml
[dev-dependencies]
pretty_assertions = "*"  # Better diff output
test-case = "*"          # Parameterized tests
mockall = "*"            # Mocking
fake = "*"               # Fake data generation
```

```rust
use test_case::test_case;

#[test_case(0, 0, 0)]
#[test_case(1, 1, 2)]
#[test_case(2, 2, 4)]
fn test_add(a: i32, b: i32, expected: i32) {
    assert_eq!(add(a, b), expected);
}
```

---

## Complete Stack Example

```toml
# Cargo.toml for web service
[dependencies]
# Async
tokio = { version = "*", features = ["full"] }

# Web
axum = "*"
tower = "*"
tower-http = { version = "*", features = ["cors", "trace"] }

# Database
sqlx = { version = "*", features = ["runtime-tokio", "tls-native-tls", "postgres", "macros", "migrate"] }

# Serialization
serde = { version = "*", features = ["derive"] }
serde_json = "*"

# Error handling
thiserror = "*"
anyhow = "*"

# Observability
tracing = "*"
tracing-subscriber = { version = "*", features = ["env-filter"] }

# Config
config = "*"

# Utils
uuid = { version = "*", features = ["v4", "serde"] }
chrono = { version = "*", features = ["serde"] }

[dev-dependencies]
tokio-test = "*"
```
