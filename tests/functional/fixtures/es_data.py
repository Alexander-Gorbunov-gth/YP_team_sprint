import pytest_asyncio
import asyncio
import uuid

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
# from functional.settings import test_settings

from ..testdata.indexes import indexes, Genre

GENRE_UUID = str(uuid.uuid4())
GENRE_NAME = "GENRE_NAME"

@pytest_asyncio.fixture(name="create_es_indexes", scope='session')
def create_es_indexes(es_dsl):
    for index in indexes:
        index.init()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    print("!es_client")
    es_client = AsyncElasticsearch(
        hosts=test_settings.es_url_to_connect,
        # "http://localhost:9200/",
        verify_certs=False,
        timeout=20
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='es_write_data')
async def es_write_data(es_client):
    async def inner(data: list[dict]):
        updated, errors = await async_bulk(client=es_client, actions=data)
        await es_client.close()

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(name='add_genre')
async def add_genre(es_write_data):
    genre_data = [
        Genre(
            id=GENRE_UUID,
            name=GENRE_NAME
        )
    ]
    bulk_query: list[dict] = []
    for row in genre_data:
        data = {'_index': 'genres', '_id': row.id}
        data.update({'_source': row.to_dict()})
        bulk_query.append(data)
    await es_write_data(bulk_query)


# @pytest_asyncio.fixture(name='add_genres')
# async def add_genres(es_write):
#     data = [
#         Genre(
#             id=str(uuid.uuid4()),
#             name=f"genre_name {1}"
#         ).to_dict() for _ in range(10)
#     ]
#     await es_write(data)
