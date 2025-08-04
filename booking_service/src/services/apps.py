import abc
from datetime import timedelta
from uuid import UUID
import logging
from datetime import datetime, timezone
import httpx

from src.domain.dtos.movie import MovieGetDTO
from src.domain.entities.movie import Movie
from src.domain.entities.author import Author
from src.services.interfaces.uow import IUnitOfWork


logger = logging.getLogger(__name__)


class IAppsService(abc.ABC):
    @abc.abstractmethod
    async def get_film(self, film_id: UUID) -> Movie | None: ...


class AppsService(IAppsService):

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def get_film(self, film_id: UUID) -> Movie | None:
        async with httpx.AsyncClient() as client:
            try:
                url = f"http://content_service:8005/api/v1/films/{film_id}"
                response = await client.get(url=url, headers={"X-Request-Id": "123"})
                response.raise_for_status()
                result = response.json()
                logger.info(f"{result=}")
                return Movie(**result)
            except httpx.HTTPStatusError as e:
                logger.error(f"Ошибка при поиске фильмов: {e}")
            except httpx.RequestError as e:
                logger.error(f"Ошибка запроса к контент-сервису: {e}")
            return None

    async def get_author(self, user_id: UUID) -> Author | None:
        async with httpx.AsyncClient() as client:
            try:
                url = f"http://auth_service:8001/api/v1/auth/get-user-data/{user_id}"
                response = await client.get(url=url, headers={"X-Request-Id": "123"})
                response.raise_for_status()
                result = response.json()
                logger.info(f"{result=}")
                return Author(**result)
            except httpx.HTTPStatusError as e:
                logger.error(f"Ошибка при поиске авторов: {e}")
            except httpx.RequestError as e:
                logger.error(f"Ошибка запроса к аутентификационному сервису: {e}")
            return None
