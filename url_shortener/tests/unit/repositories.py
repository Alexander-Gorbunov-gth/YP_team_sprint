from datetime import datetime

from src.domain.entities import ShortUrl
from src.domain.exceptions import ShortUrlIsExists
from src.domain.repositories import AbstractShortUrlRepository


class FakeShortUrlRepository(AbstractShortUrlRepository):
    """Фейковый репозиторий для таблицы с сокрщением ссылок"""

    def __init__(self):
        self._rows = {}

    async def create(
        self,
        short_url: str,
        original_url: str,
        expires_at: datetime
    ) -> ShortUrl:
        if short_url in self._rows:
            raise ShortUrlIsExists
        row = ShortUrl(
            short_url=short_url,
            original_url=original_url,
            expires_at=expires_at,
        )
        self._rows[short_url] = row
        self._rows[original_url] = row
        return row

    async def get_by_original_url(self, original_url: str) -> ShortUrl | None:
        return self._rows.get(original_url)

    async def get_by_short_url(self, short_url: str) -> ShortUrl | None:
        return self._rows.get(short_url)

    async def delete_expired_urls(self) -> None:
        self._rows = {}
