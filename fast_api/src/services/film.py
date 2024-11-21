import hashlib
import json
import logging
from functools import lru_cache
from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError, ConnectionError
from fastapi import Depends
from redis.asyncio import Redis
from backoff import on_exception, expo, full_jitter

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
logger = logging.getLogger(__name__)


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_film_list(
            self,
            sort: str = '-imdb_rating',
            order: str = 'desc',
            page_size: int = 10,
            page: int = 1,
    ) -> list[Film] | None:
        """ Получаем список фильмов, кэшируем результаты. """
        search_query = self._generate_es_query(sort=sort, order=order, page_size=page_size, page=page)
        films = await self._get_films_with_query(search_query)
        if not films:
            return None
        return films

    async def get_by_id(self, film_id: str) -> Film | None:
        """ Получаем фильм по ID с кэшированием. """
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def get_films_by_query(
            self,
            query: str,
            order: str = 'desc',
            page_size: int = 10,
            page: int = 1
    ) -> list[Film] | None:
        """ Получаем фильмы по запросу с кэшированием. """
        search_query = self._generate_es_query(query=query, order=order, page_size=page_size, page=page)
        films = await self._get_films_with_query(search_query)
        if not films:
            return None
        return films

    @on_exception(expo, ConnectionError, max_tries=5, jitter=full_jitter)
    async def _get_films_with_query(self, query: dict[str, Any]) -> list[Film] | None:
        """ Получаем фильмы из Elasticsearch с кэшированием. """
        cache_key = self._generate_cache_key(query)
        films = await self._get_from_cache(cache_key)
        if films:
            return films

        try:
            result = await self.elastic.search(index='movies', body=query)
            hits = result.get('hits', {}).get('hits', [])
            if not hits:
                logger.warning('Не найдено фильмов по запросу: {}'.format(query))
                return None
            films = [Film(**film['_source']) for film in hits]
            await self._put_to_cache(cache_key, films)
            return films
        except NotFoundError as e:
            logger.warning('Невозможно найти фильмы по запросу: {}. Ошибка: {}'.format(query, e))
            return None
        except ConnectionError as e:
            logger.warning('Ошибка подключения к ElasticSearch. Ошибка {}'.format(e))
            return None

    @on_exception(expo, ConnectionError, max_tries=5, jitter=full_jitter)
    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        """ Получаем фильм из Elasticsearch. """
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
            return Film(**doc['_source'])
        except NotFoundError:
            logger.warning('Не найдено фильма по id "{}"'.format(film_id))
            return None
        except ConnectionError as e:
            logger.warning('Ошибка подключения к ElasticSearch. Ошибка {}'.format(e))
            return None

    async def _film_from_cache(self, film_id: str) -> Film | None:
        """ Получаем фильм из кэша. """
        data = await self.redis.get(film_id)
        if not data:
            return None
        return Film.parse_raw(data)

    async def _put_film_to_cache(self, film: Film):
        """ Сохраняем фильм в кэш. """
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_from_cache(self, cache_key: str) -> list[Film] | None:
        """ Получаем фильмы из кэша. """
        data = await self.redis.get(cache_key)
        if data:
            return [Film.parse_raw(film) for film in json.loads(data)]
        return None

    async def _put_to_cache(self, cache_key: str, films: list[Film]):
        """ Сохраняем фильмы в кэш. """
        await self.redis.set(cache_key, json.dumps([film.json() for film in films]), FILM_CACHE_EXPIRE_IN_SECONDS)

    @staticmethod
    def _generate_cache_key(query: dict[str, Any]) -> str:
        """ Генерация уникального ключа для кэширования запросов. """
        query_str = json.dumps(query, sort_keys=True)
        return hashlib.sha256(query_str.encode()).hexdigest()

    @staticmethod
    def _generate_es_query(
            query: str | None = None,
            sort: str = '-imdb_rating',
            order: str = 'desc',
            page_size: int = 10,
            page: int = 1,
    ) -> dict[str, Any]:
        """Генерация запроса для Elasticsearch."""
        query_body = {
            'query': {
                'bool': {
                    'must': []
                }
            },
            'sort': [],
            'from': (page - 1) * page_size,
            'size': page_size
        }

        if query is not None:
            query_body['query']['bool']['must'] = [
                {'match': {'title': query}},
                {'match': {'description': query}}
            ]

        sort_field = 'imdb_rating' if sort.startswith('-') else sort
        query_body['sort'].append({sort_field: {'order': order}})

        return query_body


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
