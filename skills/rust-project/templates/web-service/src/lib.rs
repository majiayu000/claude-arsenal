pub mod config;
pub mod db;
pub mod error;
pub mod handlers;
pub mod models;
pub mod router;
pub mod services;

use std::sync::Arc;

pub use error::{AppError, Result};

/// Application state shared across handlers
pub struct AppState {
    pub db: sqlx::PgPool,
}

impl AppState {
    pub fn new(db: sqlx::PgPool) -> Arc<Self> {
        Arc::new(Self { db })
    }
}
