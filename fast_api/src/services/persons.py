from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Query
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
# from src.main import get_redis, get_elastic
from src.models.film import Person

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: UUID) -> Person | None:
        person = await self._get_person_from_elastic(person_id)
        if not person:
            return None
        return person
    
       
    async def get_all_persons(self, name, order, limit, offset):
        persons = await self._get_all_persons_from_elastic(name, order, limit, offset)
        if not persons:
            return []
            
        return persons
    

    async def _get_person_from_elastic(self, person_id: UUID):
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])
    
    
    async def _get_all_persons_from_elastic(self, name, order, limit, offset):
        
        if name:
            # Сначала выполняем точный поиск
            es_query_exact = {
                "from": offset,
                "size": limit,
                "sort": [
                    {"full_name.raw": {"order": order}}
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"full_name.raw": name}}
                        ]
                    }
                }
            }

            try:
                # Выполняем точный поиск
                result = await self.elastic.search(index="persons", body=es_query_exact)
                persons = [
                    Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                    for hit in result["hits"]["hits"]
                ]
                
                if persons:
                    return persons

            except Exception as e:
                print(f"Ошибка при запросе точного поиска в Elasticsearch: {e}")

            # Если точных результатов нет, выполняем полнотекстовый поиск
            es_query_fuzzy = {
                "from": offset,
                "size": limit,
                "sort": [
                    {"full_name.raw": {"order": order}}
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"full_name": name}}
                        ]
                    }
                }
            }

            try:
                result = await self.elastic.search(index="persons", body=es_query_fuzzy)
                persons = [
                    Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                    for hit in result["hits"]["hits"]
                ]
                if persons:
                    return persons
                
            except Exception as e:
                print(f"Ошибка при запросе полнотекстового поиска в Elasticsearch: {e}")
                return []
        else:
            # Если название не передается выводим весь список
            es_query_for_all = {
            "from": offset,
            "size": limit,
            "sort": [
                {"full_name.raw": {"order": order}}
            ],
            "query": {
                "match_all": {}
            }
        }
        
        try:
            result = await self.elastic.search(index="persons", body=es_query_for_all)
            persons = [
                Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                for hit in result["hits"]["hits"]
            ]
            
            if persons:
                return persons
        
        except Exception as e:
            print(f"Ошибка при запросе точного поиска в Elasticsearch: {e}")    
            
@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
