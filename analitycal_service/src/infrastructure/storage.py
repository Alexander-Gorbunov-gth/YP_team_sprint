import json
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from fastapi import Depends
from redis.asyncio.client import Redis

from src.db.redis import get_redis


class AbstractStorageRepository(ABC):
    @abstractmethod
    async def add(self, key: str, value: dict[str, Any], expire: timedelta| None = None) -> None: ...

    @abstractmethod
    async def get(self, key: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...


class RedisStorageRepository(AbstractStorageRepository):
    def __init__(self, redis_client: Redis):
        self._redis = redis_client

    async def add(self, key: str, value: dict[str, Any], expire: timedelta | None = None) -> None:
        await self._redis.set(name=key, value=json.dumps(value))

    async def get(self, key: str) -> dict[str, Any] | None:
        await self._redis.get(name=key)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)


def get_storage_repository(redis: Redis = Depends(get_redis)) -> AbstractStorageRepository:
    return RedisStorageRepository(redis_client=redis)
