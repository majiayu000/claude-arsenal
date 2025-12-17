"""User API routes."""

from uuid import UUID

from fastapi import APIRouter, status

from myapp.api.deps import UserServiceDep
from myapp.models.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/{id}", response_model=User)
async def get_user(id: UUID, service: UserServiceDep) -> User:
    """Get a user by ID."""
    return await service.get(id)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep) -> User:
    """Create a new user."""
    return await service.create(data)


@router.patch("/{id}", response_model=User)
async def update_user(id: UUID, data: UserUpdate, service: UserServiceDep) -> User:
    """Update a user."""
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID, service: UserServiceDep) -> None:
    """Delete a user."""
    await service.delete(id)
