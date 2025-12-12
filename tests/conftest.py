# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app
import asyncio


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def test_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
