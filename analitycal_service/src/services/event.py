from typing import Any
from abc import ABC, abstractmethod

from fastapi import Depends

from src.infrastructure.brocker import AbstractProducerBroker, get_broker


class AbstractEventPublisherService(ABC):
    @abstractmethod
    async def handle_event(self, topic: str, data: dict[str, Any], key: str | None = None) -> None: ...

    @abstractmethod
    async def handle_event_and_wait(self, topic: str, data: dict[str, Any], key: str | None = None) -> None: ...


class EventPublisherService(AbstractEventPublisherService):
    def __init__(self, broker: AbstractProducerBroker) -> None:
        self._broker = broker

    async def handle_event(self, topic: str, data: dict[str, Any], key: str | None = None) -> None:
        if key is None:
            await self._broker.send_message(topic=topic, value=data)
        else:
            await self._broker.send_message(topic=topic, value=data, key=key)

    async def handle_event_and_wait(self, topic: str, data: dict[str, Any], key: str | None = None) -> None:
        """Публикация события с ожиданием подтверждения (например, ack от брокера)"""
        if key is None:
            await self._broker.send_message_and_wait(topic=topic, value=data)
        else:
            await self._broker.send_message_and_wait(topic=topic, value=data, key=key)


def get_event_service(broker: AbstractEventPublisherService = Depends(get_broker)) -> AbstractEventPublisherService:
    """Провайдер зависимости."""
    return EventPublisherService(broker=broker)
