# Python Project Architecture

## Project Layouts

### src Layout (Recommended)

The `src/` layout prevents import confusion and ensures you're testing installed code.

```
myapp/
├── pyproject.toml
├── src/
│   └── myapp/           # Package lives here
│       ├── __init__.py
│       └── ...
├── tests/
│   └── ...
└── docs/
```

**Why src layout?**
- Prevents accidental imports from project root
- Forces `pip install -e .` for development
- Clean separation between package and project files
- Wheel/sdist only includes `src/` contents

### Flat Layout (Simple Scripts)

For quick scripts or small tools:

```
myapp/
├── pyproject.toml
├── myapp/               # Package at root
│   ├── __init__.py
│   └── main.py
└── tests/
```

---

## Application Structure

### Web API (FastAPI)

```
src/myapp/
├── __init__.py
├── __main__.py          # python -m myapp
├── main.py              # FastAPI app factory
├── config.py            # Pydantic Settings
│
├── api/                 # HTTP layer
│   ├── __init__.py
│   ├── deps.py          # Dependency injection
│   ├── middleware.py    # Custom middleware
│   └── routes/
│       ├── __init__.py  # Router aggregation
│       ├── user.py
│       └── health.py
│
├── models/              # Pydantic schemas
│   ├── __init__.py
│   ├── base.py          # Base models
│   ├── user.py
│   └── common.py        # Shared types
│
├── services/            # Business logic
│   ├── __init__.py
│   └── user.py
│
├── repositories/        # Data access
│   ├── __init__.py
│   ├── base.py          # Repository interface
│   └── user.py
│
├── db/                  # Database
│   ├── __init__.py
│   ├── session.py       # Engine & session
│   ├── models.py        # SQLAlchemy models
│   └── migrations/      # Alembic
│
└── core/                # Shared utilities
    ├── __init__.py
    ├── exceptions.py
    ├── logging.py
    └── security.py
```

### CLI Application

```
src/mycli/
├── __init__.py
├── __main__.py          # Entry point
├── cli.py               # Click/Typer commands
├── config.py            # Configuration
│
├── commands/            # Subcommands
│   ├── __init__.py
│   ├── init.py
│   └── process.py
│
├── services/            # Business logic
│   └── ...
│
└── core/                # Shared utilities
    ├── exceptions.py
    └── logging.py
```

### Data Pipeline

```
src/pipeline/
├── __init__.py
├── main.py              # Pipeline entry
├── config.py
│
├── extractors/          # Data sources
│   ├── __init__.py
│   ├── base.py
│   └── api.py
│
├── transformers/        # Data processing
│   ├── __init__.py
│   └── clean.py
│
├── loaders/             # Data destinations
│   ├── __init__.py
│   └── db.py
│
└── models/              # Data models
    └── ...
```

---

## Dependency Flow

```
┌─────────────────────────────────────────────┐
│                    API                       │
│              (routes, deps)                  │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│                 Services                     │
│            (business logic)                  │
└─────────────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Repos   │ │ External │ │  Cache   │
    │          │ │   APIs   │ │          │
    └──────────┘ └──────────┘ └──────────┘
          │
          ▼
    ┌──────────┐
    │    DB    │
    └──────────┘
```

**Rules:**
- API layer only handles HTTP concerns
- Services contain all business logic
- Repositories abstract data access
- Lower layers never import from upper layers

---

## Module Organization

### __init__.py Exports

```python
# src/myapp/models/__init__.py
from myapp.models.user import User, UserCreate, UserUpdate
from myapp.models.common import Pagination

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "Pagination",
]
```

### Route Aggregation

```python
# src/myapp/api/routes/__init__.py
from fastapi import APIRouter

from myapp.api.routes import health, user

router = APIRouter()
router.include_router(health.router)
router.include_router(user.router, prefix="/users", tags=["users"])
```

### Entry Points

```python
# src/myapp/__main__.py
"""Allow running as: python -m myapp"""
import uvicorn

from myapp.config import settings


def main():
    uvicorn.run(
        "myapp.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
```

---

## Configuration

### Pydantic Settings

```python
# src/myapp/config.py
from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "myapp"
    debug: bool = False
    port: int = 8000

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://localhost/myapp"
    )

    # External services
    litellm_url: str = "http://localhost:4000"
    litellm_api_key: str = ""

    # Secrets (from env only, not .env file)
    secret_key: str = Field(default="changeme")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### Environment Files

```bash
# .env.example (commit this)
APP_NAME=myapp
DEBUG=false
PORT=8000
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/myapp
LITELLM_URL=http://localhost:4000
LITELLM_API_KEY=

# .env (never commit)
DATABASE_URL=postgresql+asyncpg://prod:secret@db.example.com/myapp
SECRET_KEY=super-secret-key
```

---

## Database Layer

### SQLAlchemy 2.0 Async

```python
# src/myapp/db/session.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from myapp.config import settings

engine = create_async_engine(
    str(settings.database_url),
    echo=settings.debug,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### SQLAlchemy Models

```python
# src/myapp/db/models.py
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
```

---

## Testing Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── factories.py         # Test data factories
│
├── unit/                # Unit tests (isolated)
│   ├── __init__.py
│   ├── test_services.py
│   └── test_models.py
│
├── integration/         # Integration tests (with DB)
│   ├── __init__.py
│   ├── conftest.py      # DB fixtures
│   └── test_repositories.py
│
└── e2e/                 # End-to-end tests (full API)
    ├── __init__.py
    └── test_api.py
```

### conftest.py

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient

from myapp.main import app


@pytest.fixture
async def client():
    """Async test client for API tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
    }
```

---

## Monorepo / Multi-Package

For larger projects with multiple packages:

```
myproject/
├── pyproject.toml       # Workspace config
├── uv.lock
│
├── packages/
│   ├── core/            # Shared library
│   │   ├── pyproject.toml
│   │   └── src/core/
│   │
│   ├── api/             # API service
│   │   ├── pyproject.toml
│   │   └── src/api/
│   │
│   └── worker/          # Background worker
│       ├── pyproject.toml
│       └── src/worker/
│
└── tools/               # Development tools
    └── scripts/
```

```toml
# pyproject.toml (workspace root)
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
core = { workspace = true }
```
