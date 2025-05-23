import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import connections

from ..settings import test_settings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="es_dsl", scope="session")
async def es_dsl():
    connections.create_connection(hosts=test_settings.es_url_to_connect)


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=test_settings.es_url_to_connect, verify_certs=False, timeout=20
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="http_client")
async def http_client():
    async with aiohttp.ClientSession() as session:
        yield session
