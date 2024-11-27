from functools import lru_cache
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

# from src.db.elastic import get_elastic
# from src.main import get_redis, get_elastic
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre

import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)
class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None
        return genre
    
    async def get_all_genres(self, query, order, page_size, page_number):
        genres = await self._get_all_genres_from_elastic(query, order, page_size, page_number)
        if not genres:
            return None
        return genres
    

    async def _get_genre_from_elastic(self, genre_id: UUID):
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])


    async def _get_all_genres_from_elastic(self, query, order, page_size, page_number):
        # Рассчитываем offset и size
        from_value = (page_number - 1) * page_size
        size_value = page_size
        
        def generate_query(query, exact=True):
            return {
                "from": from_value,
                "size": size_value,
                "sort": [{"name.raw": {"order": order}}],
                "query": {
                    "bool": {
                        "must": [
                            {"term" if exact else "match": {"name.raw" if exact else "name": query}}
                        ]
                    }
                }
            }

        try:
            # Если query передано, делаем точный поиск
            if query:
                es_query = generate_query(query, exact=True)
                result = await self.elastic.search(index="genres", body=es_query)
            else:
                # Если query не передано, выполняем общий запрос
                es_query = {
                    "from": from_value,
                    "size": size_value,
                    "sort": [{"name.raw": {"order": order}}],
                    "query": {
                        "match_all": {}
                    }
                }
                result = await self.elastic.search(index="genres", body=es_query)
            
            genres = [
                Genre(id=hit["_id"], name=hit["_source"]["name"])
                for hit in result["hits"]["hits"]
            ]
            
            return genres if genres else []

        except Exception as e:
            logger.error(f"Ошибка при запросе в Elasticsearch: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при запросе")


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
