import abc
from collections.abc import Sequence
from uuid import UUID

from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.domain.entities.event import Event


class IEventRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, event: EventCreateDTO) -> Event: ...

    @abc.abstractmethod
    async def update(self, event: EventUpdateDTO) -> Event | None: ...

    @abc.abstractmethod
    async def delete(self, event_id: UUID | str) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, event_id: UUID | str) -> Event | None: ...

    @abc.abstractmethod
    async def get_events_by_user_id(self, user_id: UUID | str) -> Sequence[Event]: ...

    @abc.abstractmethod
    async def get_event_list(self, event: EventGetAllDTO) -> Sequence[Event]: ...

    @abc.abstractmethod
    async def get_for_update(self, event_id: UUID | str) -> Event | None: ...

    @abc.abstractmethod
    async def get_events_by_addresses(self, addresses: list[UUID]) -> Sequence[Event]: ...
