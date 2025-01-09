import uuid
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.services.users.schemas import RoleEnum

BASE_URL = "/api/v1/roles/"


@pytest.mark.asyncio
class TestRoles:
    @pytest.mark.parametrize(
        "role_title",
        [
            RoleEnum.AUDITOR,
            RoleEnum.MANAGER,
            RoleEnum.EDITOR,
            RoleEnum.VIEWER,
            RoleEnum.MODERATOR,
        ],
    )
    async def test_create_role(self, author_client: AsyncClient, role_title):
        """Тест создания ролей с различными названиями"""
        response = await author_client.post(
            f"{BASE_URL}create_role/", params={"role_title": role_title.value}
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "id" in data
        assert data["title"] == role_title.value

    @pytest.mark.parametrize(
        "role_title, expected_status",
        [
            (RoleEnum.ADMIN.value, HTTPStatus.BAD_REQUEST),
            ("invalid_role", HTTPStatus.UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_create_role_negative_cases(
        self, author_client: AsyncClient, create_role, role_title, expected_status
    ):
        """Тест создания ролей с неверными данными"""
        response = await author_client.post(
            f"{BASE_URL}create_role/", params={"role_title": role_title}
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "role_id, expected_status",
        [
            (lambda x: x["id"], HTTPStatus.OK),
            (uuid.uuid4(), HTTPStatus.NOT_FOUND),
            ("invalid-uuid", HTTPStatus.UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_get_role_cases(
        self, author_client: AsyncClient, create_role, role_id, expected_status
    ):
        """Тест получения ролей с разными идентификаторами"""
        actual_role_id = role_id(create_role) if callable(role_id) else role_id
        response = await author_client.get(f"{BASE_URL}{actual_role_id}")
        assert response.status_code == expected_status

        if expected_status == HTTPStatus.OK:
            data = response.json()
            assert data["id"] == str(actual_role_id)
            assert data["title"] == create_role["title"]

    @pytest.mark.parametrize(
        "permissions_data",
        [
            {"permission_slug": "test_slug", "expected_status": HTTPStatus.OK},
            {
                "permission_slug": "non_existent_slug",
                "expected_status": HTTPStatus.NOT_FOUND,
            },
        ],
    )
    async def test_add_permission_cases(
        self, author_client: AsyncClient, create_role, add_permission, permissions_data
    ):
        """Тест добавления разрешений ролям с различными сценариями"""
        role_id = create_role["id"]
        permission_slug = (
            add_permission["slug"]
            if permissions_data["permission_slug"] == "test_slug"
            else permissions_data["permission_slug"]
        )

        response = await author_client.post(
            f"{BASE_URL}{role_id}/add-permissions",
            params={"permission_slug": permission_slug},
        )
        assert response.status_code == permissions_data["expected_status"]

        if permissions_data["expected_status"] == HTTPStatus.OK:
            data = response.json()
            assert "role_id" in data
            assert "permission_id" in data

            duplicate_response = await author_client.post(
                f"{BASE_URL}{role_id}/add-permissions",
                params={"permission_slug": permission_slug},
            )
            assert duplicate_response.status_code == HTTPStatus.BAD_REQUEST
