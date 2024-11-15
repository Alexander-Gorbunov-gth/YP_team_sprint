from functools import lru_cache
from typing import List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

# from src.db.elastic import get_elastic
# from src.main import get_redis, get_elastic
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Genre


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None
        return genre
    
    async def get_all_genres(self, name, order, limit, offset):
        genres = await self._get_all_genres_from_elastic(name, order, limit, offset)
        if not genres:
            return None
        return genres
    

    async def _get_genre_from_elastic(self, genre_id: UUID):
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])
    
    async def _get_all_genres_from_elastic(self, name, order, limit, offset):
        if name:
            es_query = {
                "from": offset,
                "size": limit,
                "sort": [
                    {"name.raw": {"order": order}}
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"name.raw": name}}
                        ]
                    }
                }
            }
        else:
            es_query = {
            "from": offset,
            "size": limit,
            "sort": [
                {"name.raw": {"order": order}}
            ],
            "query": {
                "match_all": {}
            }
        }
        
        try:
            result = await self.elastic.search(index="genres", body=es_query)
            genres = [
                Genre(id=hit["_id"], name=hit["_source"]["name"])
                for hit in result["hits"]["hits"]
            ]
            
            return genres if genres else []
        
        except Exception as e:
            print(f"Ошибка при запросе точного поиска в Elasticsearch: {e}")    
            

@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
