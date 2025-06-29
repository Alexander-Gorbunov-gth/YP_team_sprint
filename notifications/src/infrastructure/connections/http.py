import logging

from httpx import AsyncClient
from src.interfaces.connection import AbstractConnection

logger = logging.getLogger(__name__)


class HttpClient(AbstractConnection):
    def __init__(self) -> None:
        self.client: AsyncClient | None = None

    async def connect(self) -> None:
        """Устанавливает соединение с HTTP клиентом."""

        logger.info("Инициализация HTTP клиента...")
        self.client = AsyncClient()
        logger.info("✅ HTTP клиент успешно инициализирован")

    async def close(self) -> None:
        """Закрывает соединение с HTTP клиентом."""

        if self.client is not None:
            await self.client.aclose()
        logger.info("✅ HTTP клиент успешно закрыт")
