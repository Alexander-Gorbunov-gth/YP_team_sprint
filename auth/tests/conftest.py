import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.db.postgres import get_session
from src.db.redis import get_redis
from src.main import app

pytest_plugins = (
    "tests.functional.fixtures.db_fixtures",
    "tests.functional.fixtures.redis_fixtures",
    "tests.functional.fixtures.permission_fixtures",
    "tests.functional.fixtures.role_fixtures",
    "tests.functional.fixtures.user_fixtures",
    "tests.functional.fixtures.auth_fixtures",
)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    from tests.functional.fixtures.db_fixtures import pytest_db
    from tests.functional.fixtures.redis_fixtures import pytest_redis

    app.dependency_overrides[get_session] = pytest_db.get_session
    app.dependency_overrides[get_redis] = pytest_redis.redis_test_client

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
