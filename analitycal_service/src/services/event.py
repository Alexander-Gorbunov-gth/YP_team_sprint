from abc import ABC, abstractmethod

from fastapi import Depends

from src.core.config import settings
from src.domain.entities import ClientEvent
from src.infrastructure.brocker import AbstractProducerBroker, get_brocker


class AbstractEventService(ABC):
    @abstractmethod
    async def handle_event(self, event: ClientEvent, event_type: str) -> None: ...

    @abstractmethod
    async def handle_event_and_wait(self, event: ClientEvent, event_type: str) -> None: ...


class EventService(AbstractEventService):
    def __init__(self, brocker: AbstractProducerBroker) -> None:
        self._brocker = brocker

    async def handle_event(self, event: ClientEvent, event_type: str) -> None:
        await self._brocker.send_message(
            topic=settings.brocker.topic_name, value=event.model_dump_json(), key=event_type
        )

    async def handle_event_and_wait(self, event: ClientEvent, event_type: str) -> None:
        await self._brocker.send_message_and_wait(
            topic=settings.brocker.topic_name, value=event.model_dump(), key=event_type
        )


def get_event_service(brocker: AbstractProducerBroker = Depends(get_brocker)):
    return EventService(brocker=brocker)
