import http

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User

BASE_URL = "/api/v1"


@pytest.fixture(scope="session")
def author_data():
    """Данные для автора"""
    return {"email": "author@gmail.com", "full_name": "author", "password": "Author123"}


@pytest.fixture(scope="session")
def client_data():
    """Данные для клиента"""
    return {
        "email": "test_client@gmail.com",
        "full_name": "client",
        "password": "Client123",
    }


@pytest.fixture
def valid_user_data():
    """Данные для валидного пользователя"""
    return {
        "email": "test_user@gmail.com",
        "full_name": "Test User",
        "password": "TestUser123",
    }


@pytest.fixture
def update_user_data():
    """Данные для обновления пользователя"""
    return {
        "email": "updated_email@gmail.com",
        "full_name": "Updated Name",
        "password": "UpdatedPass123",
    }


@pytest.fixture
def invalid_user_data():
    """Невалидные данные для пользователя"""
    return [
        {
            "email": "invalid_email",
            "full_name": "Test User",
            "password": "TestUser123",
        },
        {
            "email": "test_user@gmail.com",
            "full_name": "Test User",
            "password": "weakpass",
        },
    ]


@pytest_asyncio.fixture(scope="session")
async def author_client(client, author_data):
    """Авторизованный клиент"""
    register_response = await client.post(
        f"{BASE_URL}/auth/register/", json=author_data
    )
    assert register_response.status_code == http.HTTPStatus.OK

    response = await client.post(
        f"{BASE_URL}/auth/login/",
        data={
            "email": author_data["email"],
            "password": author_data["password"],
        },
    )
    assert response.status_code == http.HTTPStatus.OK
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest_asyncio.fixture
async def create_user(author_client, client_data):
    """Создание пользователя"""
    response = await author_client.post(
        f"{BASE_URL}/users/",
        json=client_data,
    )
    assert response.status_code == http.HTTPStatus.OK

    return response.json()


@pytest_asyncio.fixture
async def get_user_by_id(author_client, create_user):
    """Получение пользователя по ID"""
    user_args = create_user["id"]
    response = await author_client.get(f"{BASE_URL}/users/{user_args}/")
    assert response.status_code == http.HTTPStatus.OK
    return response.json()


@pytest_asyncio.fixture
async def users_count(client_session: AsyncSession):
    """Подсчет пользователей в базе данных"""
    users = [
        User(
            email=f"test_{num}@gmail.com",
            password="Test12345",
            full_name=f"Harry_{num}",
            role_id=None,
        )
        for num in range(50)
    ]
    client_session.add_all(users)
    await client_session.commit()
    return len(users)
