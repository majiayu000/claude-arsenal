use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use std::sync::Arc;
use uuid::Uuid;

use crate::error::Result;
use crate::models::{CreateUserInput, UpdateUserInput, User};
use crate::services::user as user_service;
use crate::AppState;

pub async fn get(
    State(state): State<Arc<AppState>>,
    Path(id): Path<Uuid>,
) -> Result<Json<User>> {
    let user = user_service::find_by_id(&state.db, id).await?;
    Ok(Json(user))
}

pub async fn create(
    State(state): State<Arc<AppState>>,
    Json(input): Json<CreateUserInput>,
) -> Result<(StatusCode, Json<User>)> {
    let user = user_service::create(&state.db, input).await?;
    Ok((StatusCode::CREATED, Json(user)))
}

pub async fn update(
    State(state): State<Arc<AppState>>,
    Path(id): Path<Uuid>,
    Json(input): Json<UpdateUserInput>,
) -> Result<Json<User>> {
    let user = user_service::update(&state.db, id, input).await?;
    Ok(Json(user))
}

pub async fn delete(
    State(state): State<Arc<AppState>>,
    Path(id): Path<Uuid>,
) -> Result<StatusCode> {
    user_service::delete(&state.db, id).await?;
    Ok(StatusCode::NO_CONTENT)
}
