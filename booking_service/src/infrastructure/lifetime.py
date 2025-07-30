import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import clear_mappers

from src.infrastructure.models import start_mappers
from src.core.config import settings
from src.infrastructure.db import postgres
from src.interfaces.lifetime import AbstractAppLifetime

logger = logging.getLogger(__name__)


class AppLifetime(AbstractAppLifetime):
    async def startup(self) -> None:
        await self._connect_to_postgres()

    async def shutdown(self) -> None:
        await self._disconnect_from_postgres()
        clear_mappers()

    async def _connect_to_postgres(self) -> None:
        postgres.engine = create_async_engine(url=settings.postgres.connection_url, echo=settings.postgres.echo)
        postgres.session_maker = async_sessionmaker(postgres.engine, expire_on_commit=False, class_=AsyncSession)
        try:
            async with postgres.engine.begin() as _:
                logger.info("✅ Соединение с базой данных успешно установлено")
                start_mappers()
        except Exception as e:
            logger.error(
                "❌ Ошибка при установлении соединения с базой данных %s: %s", settings.postgres.connection_url, e
            )
            raise e

    async def _disconnect_from_postgres(self) -> None:
        if postgres.engine is not None:
            await postgres.engine.dispose()
        logger.info("Отключение от Postgres")
