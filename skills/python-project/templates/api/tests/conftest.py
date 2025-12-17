"""Shared test fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from myapp.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Async test client for API tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def user_data() -> dict[str, str]:
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "name": "Test User",
    }
