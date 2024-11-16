from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Query
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
# from src.main import get_redis, get_elastic
from src.models.film import Person
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

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
    
    # GET /api/v1/persons/search?query=captain&page_number=1&page_size=50

    # Настройка логирования
    logger = logging.getLogger(__name__)

    async def _get_all_persons_from_elastic(self, query, order, page_size, page_number):
        from_value = (page_number - 1) * page_size
        size_value = page_size  
        
        def generate_query(query, exact=True):
            return {
                "from": from_value,
                "size": size_value,
                "sort": [{"full_name.raw": {"order": order}}],
                "query": {
                    "bool": {
                        "must": [
                            {"term" if exact else "match": {"full_name.raw" if exact else "full_name": query}}
                        ]
                    }
                }
            }

        try:
            # Если query передано, делаем точный поиск
            if query:
                es_query = generate_query(query, exact=True) 
                result = await self.elastic.search(index="persons", body=es_query)

                persons = [
                    Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                    for hit in result["hits"]["hits"]
                ]
                
                if persons:
                    return persons

                # Если точных совпадений нет, то выполняем полнотекстовый поиск
                es_query = generate_query(query, exact=False)  
                result = await self.elastic.search(index="persons", body=es_query)
                
                persons = [
                    Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                    for hit in result["hits"]["hits"]
                ]
                if persons:
                    return persons
            
            # Если query не передано, выполняем общий запрос
            es_query = {
                "from": from_value,
                "size": size_value,
                "sort": [{"full_name.raw": {"order": order}}],
                "query": {
                    "match_all": {}
                }
            }

            # Выполняем запрос для всех персон
            result = await self.elastic.search(index="persons", body=es_query)

            persons = [
                Person(id=hit["_id"], full_name=hit["_source"]["full_name"], films=hit["_source"].get("films", []))
                for hit in result["hits"]["hits"]
            ]
            
            if persons:
                return persons
            
            raise HTTPException(status_code=404, detail="Персоны не найдены")

        except Exception as e:
            
            logger.error(f"Ошибка при запросе в Elasticsearch: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при запросе")  
                
@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
