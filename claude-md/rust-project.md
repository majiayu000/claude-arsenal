# Project Guidelines

## Tech Stack
- Language: Rust
- Build: Cargo
- Async Runtime: Tokio
- Error Handling: thiserror (library) / anyhow (application)

## Code Style
- Format with `rustfmt`
- Lint with `clippy -- -W clippy::pedantic`
- Use snake_case for variables/functions
- Use CamelCase for types/traits

## Commands
- Build: `cargo build`
- Test: `cargo test`
- Lint: `cargo clippy`
- Format: `cargo fmt`
- Run: `cargo run`

## Project Structure
```
src/
├── main.rs          # Entry point (binary)
├── lib.rs           # Library root
├── error.rs         # Error types
├── config.rs        # Configuration
└── modules/         # Feature modules
tests/               # Integration tests
benches/             # Benchmarks
```

## Conventions
- Prefer `Result<T, E>` over `panic!`
- Use `?` for error propagation
- Avoid `unwrap()` in production code
- Document public APIs with `///`
- Write tests in same file with `#[cfg(test)]`

## Dependencies Policy
- Prefer well-maintained crates
- Check security advisories with `cargo audit`
- Keep dependencies minimal
