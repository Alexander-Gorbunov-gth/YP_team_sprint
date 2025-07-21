import abc
from datetime import timedelta
from uuid import UUID

from src.domain.entities.event import Event
from src.domain.schemas.event import EventCreateSchema, EventUpdateSchema
from src.services.exceptions import EventNotFoundError, EventTimeConflictError
from src.services.interfaces.producer import IProducer, PublishMessage
from src.services.interfaces.repositories.event import IEventRepository


class IEventService(abc.ABC):
    @abc.abstractmethod
    async def create(self, event: EventCreateSchema) -> Event | None: ...

    @abc.abstractmethod
    async def update(self, event: EventUpdateSchema) -> Event | None: ...

    @abc.abstractmethod
    async def delete(self, event_id: UUID | str) -> None: ...


class EventService(IEventService):
    EVENT_DURATION_HOURS = 3

    def __init__(self, event_repository: IEventRepository, producer: IProducer):
        self._event_repository = event_repository
        self._producer = producer

    def _check_event_time_conflict(
        self, event: EventCreateSchema | EventUpdateSchema, user_events: list[Event]
    ) -> None:
        """
        Проверяет, что событие не пересекается с другими событиями пользователя.
        param: event: EventCreateSchema - событие для создания
        param: user_events: list[Event] - список событий пользователя
        """
        if event.start_datetime is not None:
            if any(
                user_event.start_datetime - timedelta(hours=self.EVENT_DURATION_HOURS)
                < event.start_datetime
                < user_event.start_datetime + timedelta(hours=self.EVENT_DURATION_HOURS)
                for user_event in user_events
            ):
                raise EventTimeConflictError("Event overlaps with existing event")

    async def create(self, event: EventCreateSchema) -> Event:
        """
        Создание события.
        Проверяется, что событие не пересекается с другими событиями пользователя.
        param: event: EventCreateSchema - событие для создания
        """

        user_events: list[Event] = await self._event_repository.get_events_by_user_id(event.owner_id)
        self._check_event_time_conflict(event, user_events)
        return await self._event_repository.create(event)

    async def update(self, event: EventUpdateSchema) -> Event | None:
        """
        Обновление события.
        Проверяется, что событие не пересекается с другими событиями пользователя.
        param: event: EventUpdateSchema - событие для обновления
        """

        current_event: Event | None = await self._event_repository.get_by_id(event.id)
        if current_event is None:
            raise EventNotFoundError("Event not found")
        current_event.can_be_updated()
        if event.start_datetime is not None:
            user_events: list[Event] = await self._event_repository.get_events_by_user_id(current_event.owner_id)
            self._check_event_time_conflict(event, user_events)
        return await self._event_repository.update(event)

    async def delete(self, event_id: UUID | str) -> None:
        """
        Удаление события.
        param: event_id: UUID | str - id события
        """

        current_event: Event | None = await self._event_repository.get_full_by_id(event_id)
        if current_event is None:
            raise EventNotFoundError("Event not found")
        for reservation in current_event.reservations:
            message = PublishMessage(user_id=reservation.user_id)
            await self._producer.publish(message=message)
        return await self._event_repository.delete(event_id)
