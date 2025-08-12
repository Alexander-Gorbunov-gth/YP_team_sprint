import asyncio
from collections.abc import Sequence
from uuid import UUID, uuid4

from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.domain.entities.event import Event
from src.services.interfaces.repositories.event import IEventRepository


class FakeEventRepository(IEventRepository):
    def __init__(self) -> None:
        self._events: list[Event] = []
        self._lock = asyncio.Lock()

    async def create(self, event: EventCreateDTO) -> Event:
        created_event = Event(**event.model_dump(), id=uuid4())
        self._events.append(created_event)
        return created_event

    async def update(self, event: EventUpdateDTO) -> Event | None:
        for i, e in enumerate(self._events):
            if e.id == event.id:
                self._events[i] = Event(**event.model_dump(), id=e.id)
                return self._events[i]
        return None

    async def delete(self, event_id: UUID | str) -> None:
        self._events = [e for e in self._events if e.id != event_id]

    async def get_by_id(self, event_id: UUID | str) -> Event | None:
        for event in self._events:
            if event.id == event_id:
                return event
        return None

    async def get_events_by_user_id(self, user_id: UUID | str) -> list[Event]:
        return [event for event in self._events if event.owner_id == user_id]

    async def get_event_list(self, event: EventGetAllDTO) -> Sequence[Event]:
        return self._events[event.offset : event.offset + event.limit]

    async def get_events_by_addresses(self, addresses: list[UUID]) -> Sequence[Event]:
        return [event for event in self._events if event.address_id in addresses]

    async def get_for_update(self, event_id: UUID | str) -> Event | None:
        await self._lock.acquire()  # Захватываем "строку"
        try:
            for event in self._events:
                if event.id == event_id:
                    return event
            return None
        finally:
            pass

    async def release_lock(self):
        if self._lock:
            self._lock.release()
            self._lock = None

