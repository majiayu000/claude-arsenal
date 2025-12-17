"""User API tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    """Test health endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, user_data: dict[str, str]) -> None:
    """Test creating a user."""
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, user_data: dict[str, str]) -> None:
    """Test getting a user by ID."""
    # Create user first
    create_response = await client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Get user
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient) -> None:
    """Test getting a non-existent user."""
    response = await client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, user_data: dict[str, str]) -> None:
    """Test updating a user."""
    # Create user first
    create_response = await client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Update user
    response = await client.patch(
        f"/api/v1/users/{user_id}",
        json={"name": "Updated Name"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, user_data: dict[str, str]) -> None:
    """Test deleting a user."""
    # Create user first
    create_response = await client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete user
    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = await client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_email(
    client: AsyncClient, user_data: dict[str, str]
) -> None:
    """Test creating user with duplicate email."""
    # Create first user
    await client.post("/api/v1/users", json=user_data)

    # Try to create duplicate
    response = await client.post("/api/v1/users", json=user_data)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CONFLICT"
