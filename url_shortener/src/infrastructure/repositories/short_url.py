
import logging
from datetime import datetime, timezone

from fastapi import Depends
from taskiq import TaskiqDepends
from sqlalchemy import Result, insert, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.domain.entities import ShortUrl
from src.domain.exceptions import ShortUrlIsExists
from src.domain.repositories import AbstractShortUrlRepository

logger = logging.getLogger(__name__)


class SQLAlchemyShortUrlRepository(AbstractShortUrlRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        short_url: str,
        original_url: str,
        expires_at: datetime
    ) -> ShortUrl:
        insert_data = {
            "short_url": short_url,
            "original_url": original_url,
            "expires_at": expires_at,
        }
        query = insert(ShortUrl).values(insert_data).returning(ShortUrl)
        try:
            result: Result = await self._session.execute(query)
            await self._commit()
        except IntegrityError:
            logger.error("Сокращённая ссылка %s уже существует.", short_url)
            raise ShortUrlIsExists
        return result.scalar_one()

    async def get_by_original_url(self, original_url: str) -> ShortUrl | None:
        query = select(ShortUrl).filter_by(original_url=original_url)
        result: Result = await self._session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_by_short_url(self, short_url: str) -> ShortUrl | None:
        query = select(ShortUrl).filter_by(short_url=short_url)
        result: Result = await self._session.execute(query)
        return result.unique().scalar_one_or_none()

    async def delete_expired_urls(self) -> None:
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        query = delete(ShortUrl).where(ShortUrl.expires_at <= current_time)
        await self._session.execute(query)
        await self._commit()

    async def _commit(self) -> None:
        await self._session.commit()


def get_short_url_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyShortUrlRepository:
    return SQLAlchemyShortUrlRepository(session=session)

def get_short_url_repository_taskiq(
    session: AsyncSession = TaskiqDepends(get_session),
) -> SQLAlchemyShortUrlRepository:
    return SQLAlchemyShortUrlRepository(session=session)
