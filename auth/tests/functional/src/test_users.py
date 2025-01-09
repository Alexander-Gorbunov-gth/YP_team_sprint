import http
import uuid

import pytest
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.roles import RolePermission
from src.models.users import User

BASE_URL = "/api/v1/users/"

INVALID_USER_DATA = [
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


@pytest.mark.asyncio
class TestUsers:
    @staticmethod
    async def _verify_user_exists(session: AsyncSession, email: str) -> bool:
        """Метод для проверки существования пользователя в базе данных"""
        stmt = select(exists().where(User.email == email))
        result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def _get_user_by_email(session: AsyncSession, email: str) -> User:
        """Метод для получения пользователя по email"""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _setup_user_permissions(
        session: AsyncSession,
        role_id: uuid.UUID,
        permission_id: uuid.UUID,
        author_email: str,
    ) -> None:
        """Метод для настройки разрешений пользователя"""
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        session.add(role_permission)

        author = await TestUsers._get_user_by_email(session, author_email)
        author.role_id = role_id
        await session.commit()

    @pytest.mark.parametrize(
        "user_data,expected_status",
        [
            (pytest.lazy_fixture("valid_user_data"), http.HTTPStatus.OK),
            *[
                (data, http.HTTPStatus.UNPROCESSABLE_ENTITY)
                for data in INVALID_USER_DATA
            ],
        ],
    )
    async def test_create_user(
        self, author_client, client_session, user_data, expected_status
    ):
        """Тест на создание пользователя с различными сценариями данных"""
        response = await author_client.post(BASE_URL, json=user_data)
        assert response.status_code == expected_status

        if expected_status == http.HTTPStatus.OK:
            data = response.json()
            assert data["email"] == user_data["email"]
            assert data["full_name"] == user_data["full_name"]

            assert await self._verify_user_exists(client_session, user_data["email"])

    @pytest.mark.parametrize(
        "user_id,expected_status",
        [
            (pytest.lazy_fixture("create_user"), http.HTTPStatus.OK),
            (uuid.uuid4(), http.HTTPStatus.NOT_FOUND),
            ("invalid-uuid", http.HTTPStatus.UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_get_user(self, author_client, user_id, expected_status):
        """Тест на получение пользователей по различным идентификаторам"""
        actual_id = user_id["id"] if isinstance(user_id, dict) else user_id
        response = await author_client.get(f"{BASE_URL}{actual_id}/")
        assert response.status_code == expected_status

        if expected_status == http.HTTPStatus.OK:
            data = response.json()
            assert data["id"] == str(actual_id)
            assert data["email"] == user_id["email"]

    @pytest.mark.parametrize(
        ("update_data", "expected_status"),
        [
            (pytest.lazy_fixture("update_user_data"), http.HTTPStatus.OK),
            *[
                (data, http.HTTPStatus.UNPROCESSABLE_ENTITY)
                for data in INVALID_USER_DATA
            ],
        ],
    )
    async def test_update_user(
        self, author_client, create_user, client_session, update_data, expected_status
    ):
        """Тест на обновление пользователя с различными сценариями данных"""
        user_id = create_user["id"]
        response = await author_client.patch(f"{BASE_URL}{user_id}/", json=update_data)
        assert response.status_code == expected_status

        if expected_status == http.HTTPStatus.OK:
            data = response.json()
            assert data["email"] == update_data["email"]
            assert data["full_name"] == update_data["full_name"]

            user = await self._get_user_by_email(client_session, update_data["email"])
            assert user is not None
            assert user.email == update_data["email"]
            assert user.full_name == update_data["full_name"]

    async def test_get_all_users_with_permission(
        self, author_client, client_session, create_role, get_permission_id, users_count
    ):
        """Тест на получение всех пользователей с корректными разрешениями"""
        await self._setup_user_permissions(
            client_session, create_role["id"], get_permission_id, "author@gmail.com"
        )

        response = await author_client.get(BASE_URL, params={"skip": 0, "limit": 50})
        assert response.status_code == http.HTTPStatus.OK
        data = response.json()
        assert len(data) == users_count

    async def test_get_all_users_without_permission(
        self, author_client, client_session
    ):
        """Тест на получение всех пользователей без корректных разрешений"""
        author = await self._get_user_by_email(client_session, "author@gmail.com")
        author.role_id = None
        await client_session.commit()

        response = await author_client.get(BASE_URL)
        assert response.status_code == http.HTTPStatus.FORBIDDEN

    @pytest.mark.parametrize(
        "skip,limit,expected_count",
        [
            (0, 10, 10),
            (10, 5, 5),
            (0, 50, None),
        ],
    )
    async def test_get_all_users_pagination(
        self,
        author_client,
        client_session,
        create_role,
        get_permission_id,
        users_count,
        skip,
        limit,
        expected_count,
    ):
        """Тест на пагинацию при получении всех пользователей"""
        await self._setup_user_permissions(
            client_session, create_role["id"], get_permission_id, "author@gmail.com"
        )

        response = await author_client.get(
            BASE_URL, params={"skip": skip, "limit": limit}
        )
        assert response.status_code == http.HTTPStatus.OK
        data = response.json()

        expected = (
            min(limit, users_count - skip + 1)
            if expected_count is None
            else expected_count
        )
        assert len(data) == expected

    async def test_add_role_to_user(self, author_client, create_user, create_role):
        """Тест на добавление роли пользователю"""
        response = await author_client.post(
            f"{BASE_URL}{create_user['id']}/add-role/",
            params={"role_id": create_role["id"]},
        )
        assert response.status_code == http.HTTPStatus.OK

        data = response.json()
        assert data["role_id"] == create_role["id"]

    async def test_add_nonexistent_role(self, author_client, create_user):
        """Тест на добавление несуществующей роли пользователю"""
        response = await author_client.post(
            f"{BASE_URL}{create_user['id']}/add-role/",
            params={"role_id": str(uuid.uuid4())},
        )
        assert response.status_code == http.HTTPStatus.NOT_FOUND

    async def test_add_role_to_nonexistent_user(self, author_client, create_role):
        """Тест на добавление роли несуществующему пользователю"""
        response = await author_client.post(
            f"{BASE_URL}{uuid.uuid4()}/add-role/",
            params={"role_id": create_role["id"]},
        )
        assert response.status_code == http.HTTPStatus.NOT_FOUND
