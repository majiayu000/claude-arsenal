use axum::Json;
use serde_json::{json, Value};

pub async fn check() -> Json<Value> {
    Json(json!({
        "status": "ok"
    }))
}
