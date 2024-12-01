from functools import lru_cache
import logging

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.redis_service import AbstractCache, RedisCache
from src.services.db_managers import DBManager, ElasticManager
from src.models.person import Person


logger = logging.getLogger(__name__)


class PersonService:
    """Класс для работы с персонами"""

    def __init__(self, redis_client: AbstractCache, elastic_client: DBManager):
        self.redis_client = redis_client
        self.elastic_client = elastic_client

    async def get_person_by_id(self, person_id: str) -> Person | None:
        """Метод для получения персоны по ID"""
        person_key = self.redis_client.get_query_key(person_id)
        person = await self.redis_client.get_object(person_key)
        if person is None:
            person = await self.elastic_client.get_object_by_id(person_id)
            if person is None:
                logger.warning("Не удалось получить персону по id %s", person_id)
                return None
            await self.redis_client.set_object(object_key=person_key, value=person)
        return Person(**person)

    async def get_person_by_query(
        self,
        query: str,
        search_fields: list,
        sort: str | None = None,
        page_size: int = 10,
        page: int = 1,
    ) -> list[Person] | None:
        """Получает список фильмов по поисковому запросу из кэша или из ES"""

        persons_key = self.redis_client.get_query_key(
            query, search_fields, sort, page_size, page
        )
        persons = await self.redis_client.get_object(object_key=persons_key)
        if persons is None:
            persons = await self.elastic_client.get_objects_by_query(
                query=query,
                fields=search_fields,
                sort=sort,
                page_size=page_size,
                page=page,
            )
            if persons is None:
                logger.warning("Данные по запросу %s не были получены.", persons_key)
                return None
            await self.redis_client.set_object(object_key=persons_key, value=persons)
        return [Person(**person) for person in persons]

    async def get_person_list(
        self, sort: str | None = None, page_size: int = 10, page: int = 1
    ) -> list[Person] | None:
        """Получает постраничный список людей из кэша или из ES"""

        persons_key = self.redis_client.get_query_key(
            sort=sort, page_size=page_size, page=page
        )
        persons = await self.redis_client.get_object(object_key=persons_key)
        if persons is None:
            persons = await self.elastic_client.get_objects_by_query(
                sort=sort, page_size=page_size, page=page
            )
            if persons is None:
                logger.warning("Данные по запросу %s не были получены.", persons_key)
                return None
            await self.redis_client.set_object(object_key=persons_key, value=persons)
        return [Person(**person) for person in persons]


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """Создает экземпляр класса PersonService для работы с персонами"""
    redis_client = RedisCache(redis)
    elastic_client = ElasticManager(elastic, "persons")
    return PersonService(redis_client=redis_client, elastic_client=elastic_client)
