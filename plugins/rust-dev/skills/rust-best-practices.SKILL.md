---
name: rust-best-practices
description: Helps write high-quality, idiomatic Rust code following Microsoft Pragmatic Rust Guidelines. Use when writing, reviewing, optimizing Rust code, or dealing with lifetimes, borrow checker, memory safety, cargo, and async Rust.
allowed-tools: Read, Grep, Glob, Edit, Bash
---
# Rust Best Practices Assistant

## Core Principles
- Prefer safe Rust; use `unsafe` only when absolutely necessary and well-documented
- Leverage the type system to prevent bugs at compile time
- Use `Result<T, E>` for error handling, avoid `panic!` in library code
- Make illegal states unrepresentable through proper type design

## Code Style
- Format all code with `rustfmt`
- Follow all `clippy` suggestions (run with `cargo clippy -- -W clippy::pedantic`)
- Use `snake_case` for variables and functions
- Use `CamelCase` for types and traits
- Use `SCREAMING_SNAKE_CASE` for constants

## Memory & Ownership
- Prefer borrowing (`&T`, `&mut T`) over ownership when possible
- Use `Cow<str>` for strings that might be borrowed or owned
- Avoid unnecessary `.clone()` - consider borrowing or restructuring
- Use `Arc<T>` for shared ownership across threads, `Rc<T>` for single-threaded

## Error Handling
- Use `thiserror` for defining library error types
- Use `anyhow` for application-level error handling
- Provide meaningful, actionable error messages
- Use `?` operator for error propagation

## Performance
- Avoid unnecessary heap allocations
- Prefer iterators over manual loops (zero-cost abstraction)
- Use `&str` instead of `String` for function parameters when possible
- Consider using `SmallVec` for small, stack-allocated vectors

## Async Rust
- Use `tokio` as the async runtime for most applications
- Prefer `async fn` over manual `Future` implementations
- Avoid blocking operations in async contexts
- Use `tokio::spawn` for concurrent tasks

## Testing
- Write unit tests in the same file using `#[cfg(test)]` module
- Use `#[should_panic]` for testing panic behavior
- Use `proptest` or `quickcheck` for property-based testing
- Aim for meaningful test coverage, not just line coverage

## Common Patterns
- Use the builder pattern for complex object construction
- Use `From` and `Into` traits for type conversions
- Implement `Default` when a sensible default exists
- Use `Option<T>` instead of sentinel values

## What to Avoid
- Avoid `unwrap()` in production code; use `expect()` with context or proper error handling
- Avoid `String` when `&str` suffices
- Avoid manual memory management when safe abstractions exist
- Avoid `unsafe` without thorough documentation and testing
