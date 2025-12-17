# Rust Project Architecture

## Module System Fundamentals

### Crate vs Module

- **Crate**: Compilation unit. Either binary (`main.rs`) or library (`lib.rs`)
- **Module**: Logical grouping within a crate. One file = one module
- **Package**: Contains `Cargo.toml`, can have multiple crates

```rust
// src/lib.rs - crate root
pub mod config;      // loads src/config.rs or src/config/mod.rs
pub mod handlers;    // loads src/handlers/mod.rs (directory)
mod internal;        // private module

// Re-export for cleaner API
pub use config::Config;
pub use handlers::router;
```

### Visibility Rules

```rust
pub struct User {           // Public struct
    pub name: String,       // Public field
    email: String,          // Private field (crate only)
    pub(crate) id: i64,     // Visible within crate
    pub(super) role: Role,  // Visible to parent module
}

pub fn create_user() { }    // Public function
fn validate() { }           // Private (module only)
pub(crate) fn internal() {} // Crate-visible
```

---

## Simple Project Structure

Best for: CLI tools, small services, single-purpose libraries.

```
myapp/
├── Cargo.toml
├── src/
│   ├── main.rs           # Binary entry point
│   ├── lib.rs            # Library root (optional but recommended)
│   ├── config.rs         # Configuration loading
│   ├── error.rs          # Error types with thiserror
│   ├── handlers/         # HTTP handlers (for web apps)
│   │   ├── mod.rs        # pub mod user; pub mod health;
│   │   ├── user.rs
│   │   └── health.rs
│   ├── services/         # Business logic
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── models/           # Domain types
│   │   ├── mod.rs
│   │   └── user.rs
│   └── db/               # Database layer
│       ├── mod.rs
│       └── queries.rs
├── tests/                # Integration tests
│   └── api_test.rs
├── benches/              # Benchmarks
│   └── perf.rs
└── examples/             # Example usage
    └── basic.rs
```

### Module Organization

```rust
// src/handlers/mod.rs
mod health;
mod user;

pub use health::*;
pub use user::*;

// Or explicit re-exports:
pub use health::health_check;
pub use user::{get_user, create_user, delete_user};
```

---

## Workspace Structure

Best for: Large projects, monorepos, multi-binary projects.

```
myapp/
├── Cargo.toml              # Workspace manifest (no [package])
├── Cargo.lock              # Single lockfile for all crates
├── crates/
│   ├── app/                # Main binary
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── main.rs
│   ├── api/                # HTTP API library
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── handlers.rs
│   │       └── router.rs
│   ├── core/               # Core domain logic
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── models.rs
│   │       └── services.rs
│   ├── db/                 # Database layer
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       └── repositories.rs
│   └── cli/                # CLI binary (optional)
│       ├── Cargo.toml
│       └── src/
│           └── main.rs
├── config/
│   ├── default.toml
│   └── production.toml
├── migrations/             # SQLx migrations
│   └── 001_init.sql
└── Makefile
```

### Workspace Cargo.toml

```toml
[workspace]
resolver = "3"
members = ["crates/*"]

# Shared package metadata
[workspace.package]
version = "0.1.0"
edition = "2024"
authors = ["Your Name <you@example.com>"]
license = "MIT"
repository = "https://github.com/you/myapp"

# Shared dependencies - define once, use everywhere
[workspace.dependencies]
# Async
tokio = { version = "*", features = ["full"] }
async-trait = "*"

# Web
axum = "*"
tower = "*"
tower-http = { version = "*", features = ["cors", "trace"] }

# Serialization
serde = { version = "*", features = ["derive"] }
serde_json = "*"

# Database
sqlx = { version = "*", features = ["runtime-tokio", "tls-native-tls", "postgres", "macros", "migrate"] }

# Error handling
thiserror = "*"
anyhow = "*"

# Observability
tracing = "*"
tracing-subscriber = { version = "*", features = ["env-filter"] }

# Testing
tokio-test = "*"

# Shared lint configuration
[workspace.lints.rust]
unsafe_code = "forbid"

[workspace.lints.clippy]
all = "warn"
pedantic = "warn"
```

### Crate Cargo.toml

```toml
# crates/app/Cargo.toml
[package]
name = "app"
version.workspace = true
edition.workspace = true

[dependencies]
# Internal crates
api = { path = "../api" }
core = { path = "../core" }
db = { path = "../db" }

# External (inherit from workspace)
tokio.workspace = true
anyhow.workspace = true
tracing.workspace = true
tracing-subscriber.workspace = true

[lints]
workspace = true
```

---

## Dependency Graph

```
┌─────────────────────────────────────────────────┐
│                     app                          │
│               (binary crate)                     │
└─────────────────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │   api   │  │   cli   │  │  worker │
    │  (lib)  │  │ (binary)│  │ (binary)│
    └─────────┘  └─────────┘  └─────────┘
          │            │            │
          └────────────┼────────────┘
                       ▼
                 ┌─────────┐
                 │  core   │
                 │  (lib)  │
                 └─────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │   db    │  │  cache  │  │  queue  │
    │  (lib)  │  │  (lib)  │  │  (lib)  │
    └─────────┘  └─────────┘  └─────────┘
```

**Rules:**
- Lower layers never depend on upper layers
- `core` contains pure business logic, no I/O
- Infrastructure crates (`db`, `cache`) implement traits from `core`
- Binary crates wire everything together

---

## ripgrep-Style Architecture

For CLI tools processing data with high performance.

```
myapp/
├── Cargo.toml            # Workspace root
├── crates/
│   ├── myapp/            # Main binary + CLI parsing
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── main.rs
│   │       └── args.rs   # CLI argument parsing
│   ├── myapp-core/       # Facade crate, coordinates others
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── myapp-parser/     # Parsing logic
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── myapp-matcher/    # Matching/filtering
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── myapp-printer/    # Output formatting
│       ├── Cargo.toml
│       └── src/lib.rs
```

**Key patterns from ripgrep:**
- Facade crate (`-core`) provides unified API
- Each sub-crate has single responsibility
- Parallel processing with work-stealing (crossbeam)
- Arc-wrapped state for shared immutable data

---

## Binary + Library Pattern

Expose both binary and library from same crate.

```
myapp/
├── Cargo.toml
├── src/
│   ├── main.rs    # Uses lib.rs
│   └── lib.rs     # All logic here
```

```toml
# Cargo.toml
[package]
name = "myapp"

[lib]
name = "myapp"
path = "src/lib.rs"

[[bin]]
name = "myapp"
path = "src/main.rs"
```

```rust
// src/main.rs
use myapp::Config;

fn main() -> anyhow::Result<()> {
    let config = Config::from_env()?;
    myapp::run(config)?;
    Ok(())
}

// src/lib.rs
pub mod config;
pub use config::Config;

pub fn run(config: Config) -> anyhow::Result<()> {
    // ...
}
```

---

## Testing Structure

### Unit Tests (Same File)

```rust
// src/services/user.rs
pub fn validate_email(email: &str) -> bool {
    email.contains('@') && email.contains('.')
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_email() {
        assert!(validate_email("test@example.com"));
    }

    #[test]
    fn test_invalid_email() {
        assert!(!validate_email("invalid"));
    }
}
```

### Integration Tests (tests/)

```rust
// tests/api_test.rs
use myapp::AppState;

#[tokio::test]
async fn test_full_workflow() {
    let state = setup_test_state().await;
    // Test against real (test) database
}
```

### Test Utilities Crate

```
crates/
├── app/
├── core/
└── test-utils/          # Shared test helpers
    ├── Cargo.toml
    └── src/
        ├── lib.rs
        ├── fixtures.rs
        └── mocks.rs
```

```toml
# crates/app/Cargo.toml
[dev-dependencies]
test-utils = { path = "../test-utils" }
```

---

## Feature Flags

```toml
[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]
sqlite = ["sqlx/sqlite"]
full = ["postgres", "mysql", "sqlite"]
```

```rust
#[cfg(feature = "postgres")]
pub mod postgres;

#[cfg(feature = "mysql")]
pub mod mysql;
```

---

## Conditional Compilation

```rust
// Platform-specific code
#[cfg(target_os = "linux")]
fn get_memory_info() -> MemInfo { /* Linux impl */ }

#[cfg(target_os = "macos")]
fn get_memory_info() -> MemInfo { /* macOS impl */ }

#[cfg(windows)]
fn get_memory_info() -> MemInfo { /* Windows impl */ }

// Test-only code
#[cfg(test)]
fn mock_service() -> MockService { }

// Debug builds only
#[cfg(debug_assertions)]
fn debug_print(msg: &str) { eprintln!("[DEBUG] {}", msg); }
```
