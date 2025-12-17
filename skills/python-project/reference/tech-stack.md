# Python Tech Stack

## Version Strategy

> **Always use latest. Never pin versions in templates.**

```toml
[project]
dependencies = [
    "fastapi",    # uv resolves latest
    "pydantic",
]
```

- `uv add` fetches latest compatible versions
- `uv.lock` ensures reproducible builds
- `uv lock --upgrade` updates all dependencies

---

## Package Management

### uv (Recommended)

Rust-based, 10-100x faster than pip. Replaces pip, pip-tools, pyenv, virtualenv.

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init myapp
cd myapp

# Set Python version (auto-installs)
echo "3.12" > .python-version

# Add dependencies
uv add fastapi pydantic
uv add --dev pytest ruff

# Run commands
uv run python script.py
uv run pytest

# Sync environment
uv sync
```

### Poetry

Mature, stable, good for library publishing.

```bash
poetry new myapp
poetry add fastapi pydantic
poetry add --group dev pytest ruff
poetry run pytest
```

### Comparison

| Feature | uv | Poetry |
|---------|-----|--------|
| Speed | 10-100x faster | Standard |
| Python management | Built-in | Requires pyenv |
| Maturity | New (2024) | Mature |
| Library publishing | Basic | Excellent |
| Lockfile | uv.lock | poetry.lock |

**Recommendation**: uv for new projects, Poetry for libraries.

---

## Linting & Formatting

### Ruff (Recommended)

Replaces Flake8 + Black + isort. 100-200x faster.

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "RUF",  # ruff-specific
]
ignore = ["E501"]  # line too long (handled by formatter)

[tool.ruff.lint.isort]
known-first-party = ["myapp"]

[tool.ruff.format]
quote-style = "double"
```

```bash
# Lint
uv run ruff check src tests

# Format
uv run ruff format src tests

# Fix auto-fixable issues
uv run ruff check --fix src tests
```

### Type Checking: mypy

```toml
[tool.mypy]
strict = true
python_version = "3.12"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

```bash
uv run mypy src
```

---

## Web Frameworks

### FastAPI (Recommended for APIs)

Modern, async, automatic OpenAPI docs.

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    email: str


@app.post("/users")
async def create_user(user: User):
    return user
```

**Pros:**
- Automatic validation (Pydantic)
- Auto-generated docs (Swagger/ReDoc)
- Dependency injection
- Async native

### Django (Full-stack)

Batteries included, admin panel, ORM.

```python
# For full web apps with templates, auth, admin
# Not recommended for pure APIs
```

### Flask

Minimal, flexible, sync by default.

```python
# For simple apps or when you need maximum flexibility
# Consider FastAPI for new projects
```

### Comparison

| Feature | FastAPI | Django | Flask |
|---------|---------|--------|-------|
| Type | API framework | Full-stack | Micro |
| Async | Native | Added | Limited |
| Validation | Pydantic | Forms | Manual |
| Docs | Auto | Manual | Manual |
| Learning | Medium | High | Low |
| Performance | Excellent | Good | Good |

---

## Data Validation

### Pydantic v2 (Recommended)

Runtime validation with type hints. Rust core for speed.

```python
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=150)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v.strip()


class User(UserCreate):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}  # For ORM
```

### Pydantic Settings

Environment configuration.

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    debug: bool = False

    model_config = {"env_file": ".env"}
```

---

## Database

### SQLAlchemy 2.0 + asyncpg (Recommended)

Async support, type hints, mature.

```python
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(100))


# Async query
async def get_user(session: AsyncSession, id: int) -> User | None:
    return await session.get(User, id)
```

### SQLModel

Pydantic + SQLAlchemy combined (by FastAPI creator).

```python
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
```

### Comparison

| Feature | SQLAlchemy 2.0 | SQLModel | Tortoise |
|---------|----------------|----------|----------|
| Async | Yes (asyncpg) | Yes | Native |
| Type hints | Excellent | Excellent | Good |
| Maturity | Very mature | New | Moderate |
| Pydantic | Separate | Built-in | Separate |

---

## HTTP Client

### httpx (Recommended)

Async support, HTTP/2, requests-compatible API.

```python
import httpx


# Async
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()


# Sync
def fetch_data_sync():
    response = httpx.get("https://api.example.com/data")
    return response.json()
```

### requests

Classic, sync-only.

```python
import requests

response = requests.get("https://api.example.com/data")
```

---

## Testing

### pytest (Recommended)

Simple, powerful, rich plugin ecosystem.

```python
import pytest


def test_add():
    assert 1 + 1 == 2


@pytest.fixture
def user_data():
    return {"name": "Test", "email": "test@example.com"}


def test_create_user(user_data):
    assert user_data["name"] == "Test"
```

### pytest-asyncio

Async test support.

```python
import pytest


@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected
```

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # No need for @pytest.mark.asyncio
```

### Key Plugins

```toml
[tool.uv]
dev-dependencies = [
    "pytest",
    "pytest-asyncio",    # Async tests
    "pytest-cov",        # Coverage
    "pytest-xdist",      # Parallel execution
    "httpx",             # Async test client
]
```

---

## Logging

### structlog (Recommended)

Structured logging, great for production.

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

logger.info("user_created", user_id=123, email="test@example.com")
# {"event": "user_created", "user_id": 123, "email": "test@example.com", "level": "info", "timestamp": "..."}
```

### loguru

Simple API, colorful output.

```python
from loguru import logger

logger.info("Processing {count} items", count=10)
```

---

## CLI Tools

### Typer (Recommended)

Click-based, type hints for arguments.

```python
import typer

app = typer.Typer()


@app.command()
def hello(name: str, count: int = 1):
    for _ in range(count):
        print(f"Hello {name}!")


if __name__ == "__main__":
    app()
```

### Click

Lower-level, more control.

```python
import click


@click.command()
@click.option("--name", required=True)
def hello(name):
    click.echo(f"Hello {name}!")
```

---

## Complete Stack Example

```toml
# pyproject.toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    # Web
    "fastapi",
    "uvicorn[standard]",

    # Validation
    "pydantic",
    "pydantic-settings",

    # Database
    "sqlalchemy[asyncio]",
    "asyncpg",
    "alembic",

    # HTTP
    "httpx",

    # Logging
    "structlog",

    # LLM
    "openai",  # For LiteLLM proxy
]

[tool.uv]
dev-dependencies = [
    # Testing
    "pytest",
    "pytest-asyncio",
    "pytest-cov",

    # Quality
    "ruff",
    "mypy",

    # Types
    "types-passlib",
]
```
