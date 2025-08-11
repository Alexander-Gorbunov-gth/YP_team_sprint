import abc
from datetime import timedelta
from uuid import UUID
import logging
from datetime import datetime, timezone
from collections.abc import Sequence

from src.domain.dtos.event import EventCreateDTO, EventUpdateDTO, EventGetAllDTO
from src.domain.entities.event import Event
from src.domain.entities.reservation import Reservation
from src.services.exceptions import (
    EventNotFoundError,
    EventTimeConflictError,
    EventStartDatetimeError,
    EventNotOwnerError,
)
from src.services.interfaces.producer import PublishMessage
from src.services.interfaces.uow import IUnitOfWork


logger = logging.getLogger(__name__)


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class IEventService(abc.ABC):
    @abc.abstractmethod
    async def create(self, event: EventCreateDTO) -> Event | None: ...

    @abc.abstractmethod
    async def update(self, event: EventUpdateDTO, user_id: UUID) -> Event | None: ...

    @abc.abstractmethod
    async def delete(self, event_id: UUID | str, user_id: UUID) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, event_id: UUID | str) -> Event: ...

    @abc.abstractmethod
    async def get_event_list(self, event_params: EventGetAllDTO) -> list[Event]: ...

    @abc.abstractmethod
    async def get_events_by_user_id(self, user_id: UUID) -> list[Event]: ...

    @abc.abstractmethod
    async def reserve_seats(
        self, event_id: UUID | str, user_id: UUID, seats: int
    ) -> Reservation: ...

    @abc.abstractmethod
    async def get_nearby_events(
        self, latitude: float, longitude: float, radius: float = 3_000.0
    ) -> Sequence[Event]: ...


class EventService(IEventService):
    EVENT_DURATION_HOURS = 3

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def _notify_user(
        self, user_id: UUID, event_type: str, channels: list[str]
    ) -> None:
        """
        Отправляет уведомление пользователю.
        param: user_id: UUID - id пользователя
        param: event_type: str - тип события
        param: channels: list[str] - каналы уведомлений
        """

        message = PublishMessage(
            user_id=user_id,
            event_type=event_type,
            channels=channels,
        )
        # await self._uow.producer.publish(message=message, routing_key="example")

    def _check_event_exists(self, event: Event | None) -> Event:
        """
        Проверяет, что событие существует.
        param: event_id: UUID | str - id события
        """
        if event is None:
            raise EventNotFoundError("Event not found")
        return event

    def _check_event_owner(self, event: Event, user_id: UUID) -> None:
        """
        Проверяет, что пользователь является владельцем события.
        param: event: Event - событие
        param: user_id: UUID - id пользователя
        """
        if event.owner_id != user_id:
            raise EventNotOwnerError("User is not the owner of the event")

    def _check_event_start_datetime(
        self, event: EventCreateDTO | EventUpdateDTO
    ) -> None:
        """
        Проверяет, что дата начала события не в прошлом.
        param: event: EventCreateSchema - событие для создания
        """
        if event.start_datetime is not None:
            if event.start_datetime < datetime.now(timezone.utc):
                raise EventStartDatetimeError("Event start datetime is in the past")

    def _check_event_time_conflict(
        self, event: EventCreateDTO | EventUpdateDTO, user_events: list[Event]
    ) -> None:
        """
        Проверяет, что событие не пересекается с другими событиями пользователя.
        param: event: EventCreateSchema - событие для создания
        param: user_events: list[Event] - список событий пользователя
        """
        logger.info(f"Checking time conflict for event: {event=} - {user_events=}")
        if event.start_datetime is not None:
            if any(
                (
                    (
                        to_utc(user_event.start_datetime)
                        - timedelta(hours=self.EVENT_DURATION_HOURS)
                        < to_utc(event.start_datetime)
                        < to_utc(user_event.start_datetime)
                        + timedelta(hours=self.EVENT_DURATION_HOURS)
                    )
                    and user_event.id != event.id
                    if isinstance(event, EventUpdateDTO)
                    else False
                )
                for user_event in user_events
            ):
                raise EventTimeConflictError(
                    "Нельзя изменить мероприятие за 3 дня до его начала или если оно уже началось."
                )

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
            self._check_event_start_datetime(event)
            return await uow.event_repository.create(event)

    async def update(self, event: EventUpdateDTO, user_id: UUID) -> Event | None:
        """
        Обновление события.
        Проверяется, что событие не пересекается с другими событиями пользователя.
        param: event: EventUpdateSchema - событие для обновления
        """

        async with self._uow as uow:
            current_event: Event | None = await uow.event_repository.get_by_id(
                event_id=event.id
            )
            logger.info(f"{current_event=}")

            current_event = self._check_event_exists(current_event)
            self._check_event_owner(current_event, user_id)
            current_event.can_be_updated()
            if event.start_datetime is not None:
                user_events: list[Event] = (
                    await uow.event_repository.get_events_by_user_id(
                        current_event.owner_id
                    )
                )
                self._check_event_time_conflict(event, user_events)
                for reservation in current_event.reservations:
                    await self._notify_user(
                        reservation.user_id, "event_updated", ["email", "push"]
                    )
            return await uow.event_repository.update(event)

    async def delete(self, event_id: UUID | str, user_id: UUID) -> None:
        """
        Удаление события.
        param: event_id: UUID | str - id события
        """

        async with self._uow as uow:
            current_event: Event | None = await uow.event_repository.get_by_id(event_id)
            if current_event is None:
                raise EventNotFoundError("Event not found")
            if user_id != current_event.owner_id:
                raise EventNotOwnerError("User is not the owner of the event")
            for reservation in current_event.reservations:
                await self._notify_user(
                    reservation.user_id, "event_deleted", ["email", "push"]
                )
            return await uow.event_repository.delete(event_id)

    async def get_by_id(self, event_id: UUID | str) -> Event:
        """
        Получение события по id.
        param: event_id: UUID | str - id события
        :return: Event
        """

        async with self._uow as uow:
            event = await uow.event_repository.get_by_id(event_id)
            if event is None:
                logger.warning("Event with id=%s not found", event_id)
                raise EventNotFoundError("Event not found")
            return event

    async def get_event_list(self, event_params: EventGetAllDTO) -> list[Event]:
        """
        Получение списка событий.
        param: event_params: EventGetAllDTO - параметры события
        :return: list[Event]
        """

        async with self._uow as uow:
            return await uow.event_repository.get_event_list(event=event_params)

    async def get_events_by_user_id(self, user_id: UUID) -> list[Event]:
        """
        Получение списка событий по id пользователя.
        param: user_id: UUID - id пользователя
        :return: list[Event]
        """

        async with self._uow as uow:
            return await uow.event_repository.get_events_by_user_id(user_id)

    async def reserve_seats(
        self, event_id: UUID | str, user_id: UUID, seats: int
    ) -> Reservation:
        """
        Бронирование мест на событии.
        param: event_id: UUID | str - id события
        param: user_id: UUID - id пользователя
        param: seats: int - количество мест
        :return: Reservation
        """
        async with self._uow as uow:
            event = await uow.event_repository.get_for_update(event_id=event_id)
            event = self._check_event_exists(event)
            reservation = event.reserve(user_id=user_id, seats_requested=seats)
            created_reservation = await uow.reservation_repository.create(
                reservation=reservation
            )
            event.add_reservasion(created_reservation)
            return created_reservation

    async def get_nearby_events(
        self, latitude: float, longitude: float, radius: float = 3_000.0
    ) -> Sequence[Event]:
        """
        Получение списка событий в радиусе 3 км от заданной точки.
        :param latitude: Широта
        :param longitude: Долгота
        :param radius: Радиус в метрах
        :return: Список событий
        """

        async with self._uow as uow:
            addresses = await uow.address_repository.get_nearby_addresses(
                latitude, longitude, radius
            )
            address_ids = [address.id for address in addresses]
            events = await uow.event_repository.get_events_by_addresses(address_ids)
            return events
