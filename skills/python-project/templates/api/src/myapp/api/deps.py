"""Dependency injection for API routes."""

from typing import Annotated

from fastapi import Depends

from myapp.services.user import UserService

# Singleton service instance (in real app, would use proper DI)
_user_service: UserService | None = None


def get_user_service() -> UserService:
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service


# Type aliases for cleaner route signatures
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
