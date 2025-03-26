from abc import ABC, abstractmethod

from fastapi import Depends

from src.core.config import settings
from src.domain.entities import ClientEvent
from src.infrastructure.producer import AbstractProducerBroker, get_producer


class AbstractEventService(ABC):
    @abstractmethod
    async def handle_event(self, event: ClientEvent, event_type: str) -> None: ...

    @abstractmethod
    async def handle_event_and_wait(self, event: ClientEvent, event_type: str) -> None: ...


class EventService(AbstractEventService):
    def __init__(self, producer: AbstractProducerBroker) -> None:
        self._producer = producer

    async def handle_event(self, event: ClientEvent, event_type: str) -> None:
        await self._producer.send_message(topic=settings.producer.topic_name, value=event.model_dump(), key=event_type)

    async def handle_event_and_wait(self, event: ClientEvent, event_type: str) -> None:
        await self._producer.send_message_and_wait(
            topic=settings.producer.topic_name, value=event.model_dump(), key=event_type
        )


def get_event_service(producer: AbstractProducerBroker = Depends(get_producer)):
    return EventService(producer=producer)
