"""User models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    """Request model for creating a user."""

    pass


class UserUpdate(BaseModel):
    """Request model for updating a user."""

    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=2, max_length=100)


class User(UserBase):
    """Response model for user."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
