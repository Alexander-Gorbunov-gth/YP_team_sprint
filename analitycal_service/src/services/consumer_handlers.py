import logging
from abc import ABC, abstractmethod
from typing import Any

from src.core.config import settings

logger = logging.getLogger(__name__)


class AbstractConsumerHandler(ABC):
    @abstractmethod
    async def handle(self, topic: str, message: dict[str, Any], key: str | None = None) -> None: ...


class AuthConsumerHandler(AbstractConsumerHandler):

    async def handle(self, topic, message, key: str | None = None):
        logger.debug("Пришло сообщение из топика %s и ключем %s", topic, key)
        if key is None or key != settings.brocker.auth_topic_key:
            logger.debug("Ключ топика не подходит")
            return
