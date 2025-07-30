import abc
from uuid import UUID

from src.api.v1.schemas.event import EventCreateSchema, EventUpdateSchema
from src.domain.entities.event import Event


class IEventRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, event: EventCreateSchema) -> Event: ...

    @abc.abstractmethod
    async def update(self, event_id: UUID | str, event: EventUpdateSchema) -> Event | None: ...

    @abc.abstractmethod
    async def delete(self, event_id: UUID | str) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, event_id: UUID | str) -> Event | None: ...

    @abc.abstractmethod
    async def get_events_by_user_id(self, user_id: UUID | str) -> list[Event]: ...

    @abc.abstractmethod
    async def get_event_list(self, offset: int, limit: int) -> list[Event]: ...
