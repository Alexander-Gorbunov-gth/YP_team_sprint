import abc
from datetime import timedelta
from uuid import UUID

from src.domain.dtos.event import EventCreateDTO, EventUpdateDTO, EventGetAllDTO
from src.core.config import settings

from src.domain.entities.event import Event
from src.services.exceptions import EventNotFoundError, EventTimeConflictError
from src.services.interfaces.producer import PublishMessage
from src.services.interfaces.uow import IUnitOfWork


class IEventService(abc.ABC):
    @abc.abstractmethod
    async def create(self, event: EventCreateDTO) -> Event | None: ...

    @abc.abstractmethod
    async def update(self, event: EventUpdateDTO) -> Event | None: ...

    @abc.abstractmethod
    async def delete(self, event_id: UUID | str) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, event_id: UUID | str) -> Event: ...

    @abc.abstractmethod
    async def get_event_list(self, event: EventGetAllDTO) -> list[Event]: ...

    @abc.abstractmethod
    async def get_events_by_user_id(self, user_id: UUID) -> list[Event]: ...


class EventService(IEventService):
    EVENT_DURATION_HOURS = 3

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    def _check_event_time_conflict(self, event: EventCreateDTO | EventUpdateDTO, user_events: list[Event]) -> None:
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

    async def create(self, event: EventCreateDTO) -> Event:
        """
        Создание события.
        Проверяется, что событие не пересекается с другими событиями пользователя.
        param: event: EventCreateSchema - событие для создания
        """
        async with self._uow as uow:
            user_events: list[Event] = await uow.event_repository.get_events_by_user_id(
                event.owner_id
            )
            self._check_event_time_conflict(event, user_events)
            return await uow.event_repository.create(event)

    async def update(self, event: EventUpdateDTO) -> Event | None:
        """
        Обновление события.
        Проверяется, что событие не пересекается с другими событиями пользователя.
        param: event: EventUpdateSchema - событие для обновления
        """

        async with self._uow as uow:
            current_event: Event | None = await uow.event_repository.get_by_id(event.id)
            if current_event is None:
                raise EventNotFoundError("Event not found")
            current_event.can_be_updated()
            if event.start_datetime is not None:
                user_events: list[Event] = await uow.event_repository.get_events_by_user_id(current_event.owner_id)
                self._check_event_time_conflict(event, user_events)
                await uow.producer.publish(
                    message=PublishMessage(
                        user_id=current_event.owner_id, event_type="example", channels=["email", "push"]
                    )
                )
            return await uow.event_repository.update(event)

    async def delete(self, event_id: UUID | str) -> None:
        """
        Удаление события.
        param: event_id: UUID | str - id события
        """

        async with self._uow as uow:
            current_event: Event | None = await uow.event_repository.get_by_id(event_id)
            if current_event is None:
                raise EventNotFoundError("Event not found")
            for reservation in current_event.reservations:
                message = PublishMessage(
                    event_type="example",
                    channels=["email", "push"],
                    user_id=reservation.user_id,
                )
                await uow.producer.publish(message=message)

            return await uow.event_repository.delete(event_id)

    async def get_by_id(self, event_id: UUID | str) -> Event:
        async with self._uow as uow:
            current_event: Event | None = await uow.event_repository.get_by_id(event_id)
            if current_event is None:
                raise EventNotFoundError("Event not found")
            return current_event

    async def get_event_list(self, event: EventGetAllDTO) -> list[Event]:
        async with self._uow as uow:
            current_events: list[Event] = await uow.event_repository.get_event_list(event)
            if not current_events:
                raise EventNotFoundError("Events not found")
            return current_events

    async def get_events_by_user_id(self, user_id: UUID) -> list[Event]:
        async with self._uow as uow:
            current_events: list[Event] = await uow.event_repository.get_events_by_user_id(user_id)
            if not current_events:
                raise EventNotFoundError("Events not found")
            return current_events
