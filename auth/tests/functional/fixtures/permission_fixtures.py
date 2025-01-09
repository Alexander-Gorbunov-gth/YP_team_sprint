from http import HTTPStatus

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.permissions import Permission

BASE_URL = "/api/v1/permissions/"


@pytest.fixture
def permission_data():
    """Возвращает данные для создания нового разрешения."""
    return {
        "slug": "edit.users",
        "title": "Тестовое название",
        "description": "Тестовое описание",
    }


@pytest.fixture
def update_permission_data():
    """Возвращает данные для обновления разрешения."""
    return {"title": "Изменённое название", "description": "Изменённое описание"}


@pytest_asyncio.fixture
async def add_permission(author_client, permission_data):
    """Создаёт новое разрешение через API и возвращает его данные."""
    response = await author_client.post(BASE_URL, json=permission_data)
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest_asyncio.fixture
async def get_permission_id(client_session, author_client, add_permission):
    """Получает ID разрешения по его slug через базу данных."""
    permission_slug = add_permission["slug"]
    response = await author_client.get(f"{BASE_URL}{permission_slug}/")
    assert response.status_code == HTTPStatus.OK

    stmt = select(Permission.id).where(Permission.slug == permission_slug)
    result = await client_session.execute(stmt)
    return result.scalar_one()


@pytest_asyncio.fixture
async def permission_counts(client_session: AsyncSession):
    """Создаёт 60 тестовых разрешений в базе данных и возвращает их количество."""
    permission = [
        Permission(
            slug=f"test_slug_{num}",
            title="Тестовое название",
            description="Тестовое описание",
        )
        for num in range(60)
    ]
    client_session.add_all(permission)
    await client_session.commit()
    return len(permission)
