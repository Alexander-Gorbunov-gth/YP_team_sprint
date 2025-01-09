import pytest_asyncio
from redis.asyncio import Redis

from tests.functional.settings import test_settings


class TestRedis:
    def __init__(self, settings):
        self.host = settings.redis.redis_host
        self.port = settings.redis.redis_port

    async def redis_test_client(self):
        client = Redis(host=self.host, port=self.port)
        try:
            yield client
        finally:
            await client.aclose()


pytest_redis = TestRedis(settings=test_settings)


@pytest_asyncio.fixture
async def redis_client():
    async for client in pytest_redis.redis_test_client():
        yield client
