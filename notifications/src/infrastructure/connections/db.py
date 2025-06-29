import logging

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.interfaces.connection import AbstractConnection

logger = logging.getLogger(__name__)


class AsyncDatabase(AbstractConnection):
    def __init__(self, connection_url: str) -> None:
        self.connection_url = connection_url

        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker | None = None

    async def connect(self) -> async_sessionmaker:
        """Устанавливает соединение с базой данных."""

        logger.info("Инициализация соединения с базой данных...")
        self._engine = create_async_engine(self.connection_url)
        self._session_factory = async_sessionmaker(self._engine)
        try:
            async with self._engine.connect() as _:
                logger.info("✅ Соединение с базой данных успешно установлено")
        except Exception as e:
            logger.error("❌ Ошибка при установлении соединения с базой данных %s: %s", self.connection_url, e)
            raise e
        return self._session_factory

    async def close(self) -> None:
        """Закрывает соединение с базой данных."""

        if self._engine is not None:
            await self._engine.dispose()
        logger.info("✅ Соединение с базой данных закрыто")
