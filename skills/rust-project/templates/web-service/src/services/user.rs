use sqlx::PgPool;
use uuid::Uuid;

use crate::error::{AppError, OptionExt, Result};
use crate::models::{CreateUserInput, UpdateUserInput, User};

pub async fn find_by_id(db: &PgPool, id: Uuid) -> Result<User> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(db)
        .await?
        .or_not_found("user")
}

pub async fn find_by_email(db: &PgPool, email: &str) -> Result<Option<User>> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE email = $1", email)
        .fetch_optional(db)
        .await?;
    Ok(user)
}

pub async fn create(db: &PgPool, input: CreateUserInput) -> Result<User> {
    // Check if email already exists
    if find_by_email(db, &input.email).await?.is_some() {
        return Err(AppError::conflict("email already exists"));
    }

    let user = sqlx::query_as!(
        User,
        r#"
        INSERT INTO users (id, email, name, created_at, updated_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        RETURNING *
        "#,
        Uuid::new_v4(),
        input.email,
        input.name
    )
    .fetch_one(db)
    .await?;

    Ok(user)
}

pub async fn update(db: &PgPool, id: Uuid, input: UpdateUserInput) -> Result<User> {
    // Check user exists
    find_by_id(db, id).await?;

    // Check email uniqueness if updating email
    if let Some(ref email) = input.email {
        if let Some(existing) = find_by_email(db, email).await? {
            if existing.id != id {
                return Err(AppError::conflict("email already exists"));
            }
        }
    }

    let user = sqlx::query_as!(
        User,
        r#"
        UPDATE users
        SET email = COALESCE($2, email),
            name = COALESCE($3, name),
            updated_at = NOW()
        WHERE id = $1
        RETURNING *
        "#,
        id,
        input.email,
        input.name
    )
    .fetch_one(db)
    .await?;

    Ok(user)
}

pub async fn delete(db: &PgPool, id: Uuid) -> Result<()> {
    let result = sqlx::query!("DELETE FROM users WHERE id = $1", id)
        .execute(db)
        .await?;

    if result.rows_affected() == 0 {
        return Err(AppError::not_found("user"));
    }

    Ok(())
}
