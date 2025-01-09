from http import HTTPStatus

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.roles import Role
from src.services.users.schemas import RoleEnum

BASE_URL = "/api/v1/roles"


@pytest.fixture(scope="session")
def role_data():
    """Возвращает данные для создания роли."""
    return {"role_title": RoleEnum.ADMIN.value}


@pytest_asyncio.fixture
async def create_role(author_client: AsyncClient, role_data: dict):
    """Создает новую роль через API и возвращает данные роли."""
    response = await author_client.post(
        f"{BASE_URL}/create_role/", params={"role_title": role_data["role_title"]}
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest_asyncio.fixture
async def roles_count(client_session: AsyncSession):
    """Создает первые 5 ролей из перечисления RoleEnum и возвращает их количество."""
    roles = [Role(title=role_enum) for role_enum in list(RoleEnum)[:5]]
    client_session.add_all(roles)
    await client_session.commit()
    return len(roles)
