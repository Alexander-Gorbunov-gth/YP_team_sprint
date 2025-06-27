from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.entities import ShortUrl


class AbstractShortUrlRepository(ABC):
    @abstractmethod
    async def create(
        self,
        short_url: str,
        original_url: str,
        expires_at: datetime
    ) -> ShortUrl:
        raise NotImplementedError

    @abstractmethod
    async def get_by_original_url(self, original_url: str) -> ShortUrl | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_short_url(self, short_url: str) -> ShortUrl | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_expired_urls(self) -> None:
        raise NotImplementedError
