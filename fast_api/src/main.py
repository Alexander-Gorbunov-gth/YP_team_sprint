from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import films, genres, persons
from src.core import config
from src.db import elastic, redis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# import aioredis
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = aioredis.from_url("redis://redis")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield
    
# # Глобальные переменные для Redis и Elasticsearch
# redis: Optional[Redis] = None
# elastic: Optional[AsyncElasticsearch] = None

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     # global redis, elastic
#     # Подключение к Redis
#     redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield
    # # Подключение к Elasticsearch
    # elastic = AsyncElasticsearch(hosts=[f"http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"])

    # yield  
    
    # # Закрытие соединений при завершении работы
    # await redis.close()
    # await elastic.close()

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    # lifespan=lifespan
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])