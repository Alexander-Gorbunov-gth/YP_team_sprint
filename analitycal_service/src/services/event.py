from abc import ABC, abstractmethod
from typing import Any

from fastapi import Depends
from src.infrastructure.producer import AbstractProducerBroker, get_producer


class AbstractEventPublisherService(ABC):
    @abstractmethod
    async def handle_event(self, topic: str, data: dict[str, Any], key: str | None = None) -> None: ...

    @abstractmethod
    async def handle_event_and_wait(self, topic: str, data: dict[str, Any], key: str | None = None) -> None: ...


class EventPublisherService(AbstractEventPublisherService):
    def __init__(self, producer: AbstractProducerBroker) -> None:
        self._producer = producer

    async def handle_event(self, topic: str, data: dict[str, Any], key: str | None = None) -> None:
        """Публикация события без ожидания подтверждения"""
        await self._producer.send_message(topic=topic, value=data, key=key)

    async def handle_event_and_wait(self, topic: str, data: dict[str, Any], key: str | None = None) -> None:
        """Публикация события с ожиданием подтверждения"""
        await self._producer.send_message_and_wait(topic=topic, value=data, key=key)


def get_event_service(producer: AbstractProducerBroker = Depends(get_producer)) -> AbstractEventPublisherService:
    """Провайдер зависимости."""
    return EventPublisherService(producer=producer)
