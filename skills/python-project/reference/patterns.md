# Python Design Patterns

## Dependency Injection (FastAPI)

FastAPI's `Depends` for clean dependency management.

### Basic Dependencies

```python
# src/myapp/api/deps.py
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.db.session import async_session
from myapp.repositories.user import UserRepository
from myapp.services.user import UserService


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repo)


# Type aliases for cleaner signatures
SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

### Using Dependencies

```python
# src/myapp/api/routes/user.py
from fastapi import APIRouter

from myapp.api.deps import UserServiceDep
from myapp.models.user import User, UserCreate

router = APIRouter()


@router.post("/users", response_model=User)
async def create_user(
    data: UserCreate,
    service: UserServiceDep,
):
    return await service.create(data)
```

---

## Repository Pattern

Abstract data access for testability.

### Base Repository

```python
# src/myapp/repositories/base.py
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.db.models import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> ModelT | None:
        return await self.session.get(self.model, id)

    async def get_all(self, *, skip: int = 0, limit: int = 100) -> list[ModelT]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.session.delete(obj)
        await self.session.commit()
```

### Concrete Repository

```python
# src/myapp/repositories/user.py
from sqlalchemy import select

from myapp.db.models import UserModel
from myapp.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()
```

---

## Service Pattern

Business logic layer, framework-agnostic.

```python
# src/myapp/services/user.py
from uuid import UUID

from myapp.core.exceptions import ConflictError, NotFoundError
from myapp.db.models import UserModel
from myapp.models.user import UserCreate, UserUpdate
from myapp.repositories.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get(self, id: UUID) -> UserModel:
        user = await self.repo.get(id)
        if not user:
            raise NotFoundError("user", str(id))
        return user

    async def create(self, data: UserCreate) -> UserModel:
        # Business rule: email must be unique
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictError("email already exists")

        user = UserModel(
            email=data.email,
            name=data.name,
        )
        return await self.repo.create(user)

    async def update(self, id: UUID, data: UserUpdate) -> UserModel:
        user = await self.get(id)

        # Check email uniqueness if updating
        if data.email and data.email != user.email:
            existing = await self.repo.get_by_email(data.email)
            if existing:
                raise ConflictError("email already exists")

        # Update fields
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self.repo.session.commit()
        await self.repo.session.refresh(user)
        return user

    async def delete(self, id: UUID) -> None:
        user = await self.get(id)
        await self.repo.delete(user)
```

---

## Custom Exceptions

Structured error handling.

```python
# src/myapp/core/exceptions.py
from typing import Any


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        context: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} not found: {id}",
            code="NOT_FOUND",
            status_code=404,
            context={"resource": resource, "id": id},
        )


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
        )


class ValidationError(AppError):
    def __init__(self, message: str, errors: list[dict] | None = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            context={"errors": errors or []},
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "unauthorized"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )
```

### Exception Handler

```python
# src/myapp/api/middleware.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from myapp.core.exceptions import AppError


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "code": exc.code,
                    **exc.context,
                }
            },
        )
```

---

## Pydantic Patterns

### Base Models

```python
# src/myapp/models/base.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AppModel(BaseModel):
    """Base model with common config."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime


class IDModel(BaseModel):
    id: UUID
```

### Request/Response Models

```python
# src/myapp/models/user.py
from myapp.models.base import AppModel, IDModel, TimestampMixin


class UserBase(AppModel):
    email: str
    name: str


class UserCreate(UserBase):
    """Request model for creating user."""
    pass


class UserUpdate(AppModel):
    """Request model for updating user (all fields optional)."""
    email: str | None = None
    name: str | None = None


class User(UserBase, IDModel, TimestampMixin):
    """Response model with all fields."""
    pass
```

### Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain digit")
        return v
```

---

## Async Patterns

### Async Context Manager

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx


@asynccontextmanager
async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client


# Usage
async def fetch_data(url: str) -> dict:
    async with get_http_client() as client:
        response = await client.get(url)
        return response.json()
```

### Concurrent Tasks

```python
import asyncio


async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

### TaskGroup (Python 3.11+)

```python
import asyncio


async def process_items(items: list[str]) -> list[str]:
    results = []

    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_one(item, results))

    return results
```

### Semaphore for Rate Limiting

```python
import asyncio

import httpx


async def fetch_with_limit(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

---

## Factory Pattern

For creating objects with complex initialization.

```python
# src/myapp/core/factories.py
from myapp.config import settings
from myapp.db.session import async_session
from myapp.repositories.user import UserRepository
from myapp.services.user import UserService


class ServiceFactory:
    @staticmethod
    async def create_user_service() -> UserService:
        async with async_session() as session:
            repo = UserRepository(session)
            return UserService(repo)


# Or using dependency injection
def create_user_service(repo: UserRepository) -> UserService:
    return UserService(repo)
```

---

## Protocol Pattern (Structural Typing)

For interfaces without inheritance.

```python
from typing import Protocol
from uuid import UUID


class UserRepositoryProtocol(Protocol):
    async def get(self, id: UUID) -> UserModel | None: ...
    async def get_by_email(self, email: str) -> UserModel | None: ...
    async def create(self, obj: UserModel) -> UserModel: ...
    async def delete(self, obj: UserModel) -> None: ...


class UserService:
    def __init__(self, repo: UserRepositoryProtocol):
        self.repo = repo


# Any class with these methods works, no inheritance needed
class InMemoryUserRepository:
    async def get(self, id: UUID) -> UserModel | None: ...
    async def get_by_email(self, email: str) -> UserModel | None: ...
    async def create(self, obj: UserModel) -> UserModel: ...
    async def delete(self, obj: UserModel) -> None: ...


# Works without explicitly implementing the protocol
service = UserService(InMemoryUserRepository())
```

---

## Unit of Work Pattern

Transaction management across repositories.

```python
# src/myapp/core/uow.py
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.repositories.user import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        await self.session.close()


# Usage
async def transfer_credits(from_id: UUID, to_id: UUID, amount: int) -> None:
    async with UnitOfWork(session) as uow:
        from_user = await uow.users.get(from_id)
        to_user = await uow.users.get(to_id)

        from_user.credits -= amount
        to_user.credits += amount

        await uow.commit()
```

---

## Summary Table

| Pattern | Use Case |
|---------|----------|
| Dependency Injection | Decouple components, testability |
| Repository | Abstract data access |
| Service | Business logic layer |
| Custom Exceptions | Structured error handling |
| Pydantic Models | Validation, serialization |
| Async Context Manager | Resource cleanup |
| Protocol | Interfaces without inheritance |
| Unit of Work | Transaction management |
