from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User

BASE_URL = "/api/v1/auth"


@pytest.mark.asyncio
class TestAuth:
    @staticmethod
    async def _verify_user_in_db(session: AsyncSession, email: str) -> User:
        """Вспомогательный метод для проверки пользователя в БД"""
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @pytest.mark.parametrize(
        "user_data, expected_status",
        [
            (pytest.lazy_fixture("valid_user_data"), HTTPStatus.OK),
            (
                {
                    "email": "invalid_email",
                    "full_name": "Test User",
                    "password": "TestUser123",
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
            ),
            (
                {
                    "email": "test@gmail.com",
                    "full_name": "Test User",
                    "password": "weak",
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
            ),
            (
                {
                    "email": "test@gmail.com",
                    "full_name": "T" * 256,
                    "password": "TestUser123",
                },
                HTTPStatus.UNPROCESSABLE_ENTITY,
            ),
        ],
    )
    async def test_register(
        self,
        client: AsyncClient,
        client_session: AsyncSession,
        user_data: dict,
        expected_status: HTTPStatus,
    ):
        """Тест регистрации пользователя с различными данными"""
        response = await client.post(f"{BASE_URL}/register/", json=user_data)
        assert response.status_code == expected_status

        if expected_status == HTTPStatus.OK:
            data = response.json()
            assert data["email"] == user_data["email"]
            assert data["full_name"] == user_data["full_name"]

            user = await self._verify_user_in_db(client_session, user_data["email"])
            assert user is not None
            assert user.email == user_data["email"]

    @pytest.mark.parametrize(
        ("credentials", "expected_status", "expected_token"),
        [
            (pytest.lazy_fixture("login_data"), HTTPStatus.OK, True),
            (
                {"email": "wrong@gmail.com", "password": "TestAuth123"},
                HTTPStatus.UNAUTHORIZED,
                False,
            ),
            (
                {"email": "test_auth@gmail.com", "password": "WrongPass123"},
                HTTPStatus.UNAUTHORIZED,
                False,
            ),
            (
                {"email": "invalid_email", "password": "TestAuth123"},
                HTTPStatus.UNAUTHORIZED,
                False,
            ),
        ],
    )
    async def test_login(
        self,
        client: AsyncClient,
        valid_user_data: dict,
        credentials: dict,
        expected_status: HTTPStatus,
        expected_token: bool,
    ):
        """Тест функционала логина с различными учетными данными"""
        if expected_token:
            await client.post(f"{BASE_URL}/register/", json=valid_user_data)

        response = await client.post(f"{BASE_URL}/login/", data=credentials)
        assert response.status_code == expected_status

        if expected_token:
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "Bearer"
            assert isinstance(data["access_token"], str)

    async def test_logout_success(self, auth_client: AsyncClient):
        """Тест успешного логаута"""
        response = await auth_client.post(f"{BASE_URL}/logout/")
        assert response.status_code == HTTPStatus.NO_CONTENT

        test_response = await auth_client.get("/api/v1/users/")
        assert test_response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_logout_without_token(self, client: AsyncClient):
        """Тест логаута без токена аутентификации"""
        response = await client.post(f"{BASE_URL}/logout/")
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_duplicate_registration(
        self, client: AsyncClient, valid_user_data: dict
    ):
        """Тест попытки повторной регистрации"""
        await client.post(f"{BASE_URL}/register/", json=valid_user_data)
        response = await client.post(f"{BASE_URL}/register/", json=valid_user_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        "invalid_token", ["invalid_token", "Bearer invalid_token", None]
    )
    async def test_invalid_token(self, client: AsyncClient, invalid_token: str | None):
        """Тест доступа к защищенному эндпоинту с невалидным токеном"""
        headers = {"Authorization": invalid_token} if invalid_token else {}
        response = await client.get("/api/v1/users/", headers=headers)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_session_persistence(self, auth_client: AsyncClient):
        """Тест сохранения сессии между запросами"""
        response = await auth_client.get("/api/v1/users/")
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.FORBIDDEN]

    async def test_concurrent_sessions(
        self,
        client: AsyncClient,
        valid_user_data: dict,
        login_data: dict,
    ):
        """Тест множественных сессий для одного пользователя"""
        await client.post(f"{BASE_URL}/register/", json=valid_user_data)

        async def create_session():
            response = await client.post(f"{BASE_URL}/login/", data=login_data)
            return response.json()["access_token"]

        token1 = await create_session()
        token2 = await create_session()

        for token in [token1, token2]:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get("/api/v1/users/", headers=headers)
            assert response.status_code in [HTTPStatus.OK, HTTPStatus.FORBIDDEN]
