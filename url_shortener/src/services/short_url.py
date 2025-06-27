import string
import secrets
import logging
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from pydantic import HttpUrl

from fastapi import Depends
from taskiq import TaskiqDepends

from src.core.config import settings
from src.domain.entities import ShortUrl
from src.domain.exceptions import ShortUrlIsExists, ShortUrlNotFound
from src.domain.repositories import AbstractShortUrlRepository
from src.infrastructure.repositories.short_url import (
    get_short_url_repository, get_short_url_repository_taskiq
)

logger = logging.getLogger(__name__)
BASE62 = string.ascii_letters + string.digits


class ShortUrlService:
    def __init__(self, short_url_repository: AbstractShortUrlRepository):
        self._short_url_repository: AbstractShortUrlRepository = short_url_repository

    async def create_short_url(self, original_url: HttpUrl) -> HttpUrl:
        """
        Создание новой сокращённой ссылки.

        :param original_url: Ссылка, которая сокращается.
        :return: Созданный объект ShortUrl.
        """
        getted_url = await self._short_url_repository.get_by_original_url(
            original_url=str(original_url)
        )

        if not getted_url:
            expires_at = datetime.now(
                timezone.utc
            )+timedelta(days=settings.service.expires_days)

            while True:
                short_url = self._generate_short_code()
                try:
                    getted_url = await self._short_url_repository.create(
                        short_url=short_url,
                        original_url=str(original_url),
                        expires_at=expires_at.replace(tzinfo=None)
                    )
                    break
                except ShortUrlIsExists:
                    logger.warning("Повторная попытка создать сокращённую ссылку.")
                    continue

        return settings.service.domain+getted_url.short_url

    async def get_original_url(self, short_url: str) -> ShortUrl:
        """
        Получает полную ссылку на основе сокращённой.

        :param short_url: Сокращённая ссылка.
        :return: True, если аутентификация успешна.
        :raises WrongEmailOrPassword: Если учетные данные неверны.
        """

        short_url = await self._short_url_repository.get_by_short_url(
            short_url=short_url
        )
        if short_url is None:
            logger.error("Сокращённая ссылка %s не найдена.", short_url)
            raise ShortUrlNotFound
        return short_url.original_url

    async def delete_expired_urls(self) -> None:
        """
        Удаляет все просроченные сокращённые ссылки.
        """
        await self._short_url_repository.delete_expired_urls()
        logger.info("Удалены все просроченные сокращённые ссылки.")

    def _generate_short_code(self) -> str:
        return ''.join(
            secrets.choice(BASE62) for _ in range(
                settings.service.short_code_length
            )
        )


def get_short_url_service(
    short_url_repository: AbstractShortUrlRepository = Depends(
        get_short_url_repository
    ),
) -> ShortUrlService:
    return ShortUrlService(
        short_url_repository=short_url_repository
    )

def get_short_url_service_taskqi(
    short_url_repository: AbstractShortUrlRepository = TaskiqDepends(
        get_short_url_repository_taskiq
    ),
) -> ShortUrlService:
    return ShortUrlService(
        short_url_repository=short_url_repository
    )
