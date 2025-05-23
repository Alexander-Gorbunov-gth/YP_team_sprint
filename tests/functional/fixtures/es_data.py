import asyncio
import uuid

import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import BulkIndexError, async_bulk

from ..settings import test_settings
from ..testdata.indexes import Films, Genre, Person, indexes

GENRE_UUID = str(uuid.uuid4())
GENRE_NAME = "GENRE_NAME"

FILM_UUID = str(uuid.uuid4())
FILM_NAME = "FILM_NAME"

PERSON_UUID = str(uuid.uuid4())
PERSON_NAME = "FILM_NAME"


@pytest_asyncio.fixture(name="create_es_indexes", scope="session")
async def create_es_indexes(es_dsl, http_client):
    for index in indexes:
        index.init()
    pass


@pytest_asyncio.fixture(name="es_client", scope="session")
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=test_settings.es_url_to_connect, verify_certs=False
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name="es_write_data")
async def es_write_data(es_client):
    async def inner(data: list[dict]):
        updated, errors = await async_bulk(
            client=es_client, actions=data, refresh="wait_for"
        )
        await es_client.close()

        if errors:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture(name="add_genre")
async def add_genre(es_write_data):
    genre_data = [Genre(id=GENRE_UUID, name=GENRE_NAME)]
    bulk_query: list[dict] = []
    for row in genre_data:
        data = {"_index": "genres", "_id": row.id}
        data.update({"_source": row.to_dict()})
        bulk_query.append(data)
    await es_write_data(bulk_query)


@pytest_asyncio.fixture(name="add_genres")
async def add_genres(es_write_data):
    data = [
        Genre(id=str(uuid.uuid4()), name=f"genre_name {_}") for _ in range(10)
    ]
    bulk_query: list[dict] = []
    for row in data:
        data = {"_index": "genres", "_id": row.id}
        data.update({"_source": row.to_dict()})
        bulk_query.append(data)
    await es_write_data(bulk_query)


@pytest_asyncio.fixture(name="add_films")
async def add_films(es_write_data):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genres": ["Action", "Sci-Fi"],
            "title": "The Star",
            "description": "New World",
            "directors_names": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95", "name": "Ann"},
                {"id": "fb111f22-121e-44a7-b78f-b19191810fbf", "name": "Bob"},
            ],
            "writers": [
                {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
                {
                    "id": "b45bd7bc-2e16-46d5-b125-983d356768c6",
                    "name": "Howard",
                },
            ],
            "directors": [
                {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
                {
                    "id": "b45bd7bc-2e16-46d5-b125-983d356768c6",
                    "name": "Howard",
                },
            ],
        }
        for _ in range(60)
    ]
    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "movies", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    await es_write_data(bulk_query)


@pytest_asyncio.fixture(name="add_film")
async def add_film(es_write_data):
    es_data = [
        {
            "id": FILM_UUID,
            "imdb_rating": 8.5,
            "genres": ["Action", "Sci-Fi"],
            "title": FILM_NAME,
            "description": "New World",
            "directors_names": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95", "name": "Ann"},
                {"id": "fb111f22-121e-44a7-b78f-b19191810fbf", "name": "Bob"},
            ],
            "writers": [
                {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
                {
                    "id": "b45bd7bc-2e16-46d5-b125-983d356768c6",
                    "name": "Howard",
                },
            ],
            "directors": [
                {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
                {
                    "id": "b45bd7bc-2e16-46d5-b125-983d356768c6",
                    "name": "Howard",
                },
            ],
        }
    ]
    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "movies", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    await es_write_data(bulk_query)


@pytest_asyncio.fixture(name="add_persons")
async def add_persons(es_write_data):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "full_name": f"person_name {_}",
            "films": [
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f15",
                    "roles": ["writer"],
                },
            ],
        }
        for _ in range(60)
    ]
    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "persons", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    await es_write_data(bulk_query)


@pytest_asyncio.fixture(name="add_person")
async def add_person(es_write_data):
    es_data = [
        {
            "id": PERSON_UUID,
            "full_name": PERSON_NAME,
            "films": [
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f15",
                    "roles": ["writer"],
                },
            ],
        }
    ]
    bulk_query: list[dict] = []
    for row in es_data:
        data = {"_index": "persons", "_id": row["id"]}
        data.update({"_source": row})
        bulk_query.append(data)
    await es_write_data(bulk_query)
