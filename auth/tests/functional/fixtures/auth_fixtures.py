import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.fixture
def valid_user_data():
    return {
        "email": "test_auth@gmail.com",
        "full_name": "Test Auth",
        "password": "TestAuth123",
    }


@pytest.fixture
def login_data(valid_user_data):
    return {"email": valid_user_data["email"], "password": valid_user_data["password"]}


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, valid_user_data: dict, login_data: dict):
    """Фикстура для создания аутентифицированного клиента"""
    await client.post("/api/v1/auth/register/", json=valid_user_data)
    response = await client.post("/api/v1/auth/login/", data=login_data)
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
