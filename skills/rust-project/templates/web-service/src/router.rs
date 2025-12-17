use axum::{
    routing::{get, post},
    Router,
};
use std::sync::Arc;
use tower_http::trace::TraceLayer;

use crate::{handlers, AppState};

pub fn build(state: Arc<AppState>) -> Router {
    Router::new()
        // Health check
        .route("/health", get(handlers::health::check))
        // API v1
        .nest("/api/v1", api_v1())
        // Middleware
        .layer(TraceLayer::new_for_http())
        // State
        .with_state(state)
}

fn api_v1() -> Router<Arc<AppState>> {
    Router::new()
        // Users
        .route("/users", post(handlers::user::create))
        .route("/users/:id", get(handlers::user::get))
        .route("/users/:id", axum::routing::put(handlers::user::update))
        .route("/users/:id", axum::routing::delete(handlers::user::delete))
}
