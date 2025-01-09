from http import HTTPStatus

import pytest
from sqlalchemy import select, func, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.permissions import Permission

BASE_URL = "/api/v1/permissions/"


@pytest.mark.asyncio
class TestPermissions:
    @staticmethod
    async def _get_permission_count(session: AsyncSession) -> int:
        """
        Вспомогательный метод для получения общего количества разрешений.
        """
        stmt = select(func.count()).select_from(Permission)
        result = await session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def _get_permission_by_slug(session: AsyncSession, slug: str) -> Permission:
        """
        Вспомогательный метод для получения разрешения по slug.
        """
        stmt = select(Permission).where(Permission.slug == slug)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _check_permission_exists(session: AsyncSession, slug: str) -> bool:
        """
        Вспомогательный метод для проверки существования разрешения.
        """
        stmt = select(exists().where(Permission.slug == slug))
        result = await session.execute(stmt)
        return result.scalar()

    async def test_get_all_permissions(self, author_client, permission_counts: int):
        """
        Тест получения всех разрешений.
        """
        response = await author_client.get(BASE_URL)

        assert response.status_code == HTTPStatus.OK
        permissions = response.json()
        assert len(permissions) == permission_counts

        for permission in permissions:
            assert all(key in permission for key in ["slug", "title", "description"])

    async def test_create_permission(
        self, author_client, client_session: AsyncSession, permission_data: dict
    ):
        """
        Тест создания разрешения.
        """
        initial_count = await self._get_permission_count(client_session)

        response = await author_client.post(BASE_URL, json=permission_data)

        assert response.status_code == HTTPStatus.OK
        created_permission = response.json()

        assert created_permission["slug"] == permission_data["slug"]
        assert created_permission["title"] == permission_data["title"]
        assert created_permission["description"] == permission_data["description"]

        new_count = await self._get_permission_count(client_session)
        assert new_count == initial_count + 1

        permission = await self._get_permission_by_slug(
            client_session, permission_data["slug"]
        )
        assert permission is not None
        assert permission.title == permission_data["title"]

    async def test_get_permission_by_slug(
        self, author_client, client_session: AsyncSession, add_permission: dict
    ):
        """
        Тест получения разрешения по slug.
        """
        permission_slug = add_permission["slug"]
        response = await author_client.get(f"{BASE_URL}{permission_slug}/")

        assert response.status_code == HTTPStatus.OK
        permission = response.json()

        assert permission["slug"] == permission_slug
        assert permission["title"] == add_permission["title"]
        assert permission["description"] == add_permission["description"]

    async def test_update_permission(
        self,
        author_client,
        client_session: AsyncSession,
        add_permission: dict,
        update_permission_data: dict,
    ):
        """
        Тест обновления разрешения.
        """
        permission_slug = add_permission["slug"]
        response = await author_client.patch(
            f"{BASE_URL}{permission_slug}/", json=update_permission_data
        )

        assert response.status_code == HTTPStatus.OK
        updated_permission = response.json()

        assert updated_permission["title"] == update_permission_data["title"]
        assert (
            updated_permission["description"] == update_permission_data["description"]
        )

        permission = await self._get_permission_by_slug(client_session, permission_slug)
        assert permission.title == update_permission_data["title"]
        assert permission.description == update_permission_data["description"]

    async def test_delete_permission(
        self, author_client, client_session: AsyncSession, add_permission: dict
    ):
        """
        Тест удаления разрешения.
        """
        permission_slug = add_permission["slug"]
        initial_count = await self._get_permission_count(client_session)

        response = await author_client.delete(f"{BASE_URL}{permission_slug}/")

        assert response.status_code == HTTPStatus.OK

        new_count = await self._get_permission_count(client_session)
        assert new_count == initial_count - 1

        exists = await self._check_permission_exists(client_session, permission_slug)
        assert not exists

    @pytest.mark.parametrize(
        "invalid_slug",
        [
            "nonexistent-slug",
            "invalid.slug.format",
            "123",
            "",
        ],
    )
    async def test_get_nonexistent_permission(self, author_client, invalid_slug: str):
        """
        Тест получения несуществующего разрешения.
        """
        response = await author_client.get(f"{BASE_URL}{invalid_slug}/")
        assert response.status_code == HTTPStatus.NOT_FOUND

    async def test_create_duplicate_permission(
        self, author_client, add_permission: dict, permission_data: dict
    ):
        """
        Тест создания разрешения с дублирующимся slug.
        """
        response = await author_client.post(BASE_URL, json=permission_data)
        assert response.status_code == HTTPStatus.CONFLICT
