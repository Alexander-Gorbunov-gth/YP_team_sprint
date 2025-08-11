import logging
from collections.abc import Sequence
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.domain.entities.event import Event
from src.infrastructure.repositories.exceptions import EventNotFoundError
from src.services.interfaces.repositories.event import IEventRepository

logger = logging.getLogger(__name__)


class SQLAlchemyEventRepository(IEventRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, event: EventCreateDTO) -> Event:
        """
        Создает событие в базе данных.
        :param event: Схема события для создания.
        :return: Созданное событие.
        """

        query = insert(Event).values(event.model_dump()).returning(Event)
        result: Result = await self._session.execute(query)
        created_event: Event = result.unique().scalar_one()
        created_event.address
        return created_event

    async def update(self, event: EventUpdateDTO) -> Event | None:
        """
        Обновляет событие в базе данных.
        :param event: Обновлённый объект события.
        :raises EventNotFoundError: Если событие не найдено.
        :return: Обновлённое событие.
        """

        stmt = (
            update(Event)
            .where(Event.id == event.id)
            .values(**event.model_dump(exclude_unset=True, exclude_none=True))
            .returning(Event)
        )

        result = await self._session.execute(stmt)
        updated_event = result.scalar_one_or_none()
        if updated_event is None:
            raise EventNotFoundError("Событие с id=%s не найдено.", event.id)
        return updated_event

    async def delete(self, event_id: UUID | str) -> None:
        """
        Удаляет событие из базы данных.
        :param event_id: ID события в базе данных.
        :raises EventNotFoundError: Если событие не найдено.
        """

        check_query = select(Event).filter_by(id=event_id)
        result: Result = await self._session.execute(check_query)
        existing = result.unique().scalar_one_or_none()

        if existing is None:
            raise EventNotFoundError(f"Событие с {event_id=} не найдена.")

        await self._session.delete(existing)

    async def get_by_id(self, event_id: UUID | str) -> Event | None:
        """
        Получает одно событие по ID.
        :param event_id: ID события.
        :return: Модель события.
        """

        query = select(Event).filter_by(id=event_id)
        result: Result = await self._session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_for_update(self, event_id: UUID | str) -> Event | None:
        """
        Получает событие для обновления.
        :param event_id: ID события.
        :return: Модель события.
        """

        query = select(Event).filter_by(id=event_id).with_for_update(skip_locked=True)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_events_by_user_id(self, user_id: UUID | str) -> Sequence[Event]:
        """
        Получает все события пользователя.
        :param user_id: ID пользователя.
        :return: Список событий.
        """

        query = (
            select(Event).filter_by(owner_id=user_id).order_by(Event.created_at.desc())  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def get_event_list(self, event: EventGetAllDTO) -> Sequence[Event]:
        """
        Получает все события.
        :param limit: Максимальное количество событий для возврата (ограничение выборки).
        :param offset: Количество пропущенных событий с начала выборки (смещение).
        :return: Список событий.
        """

        query = (
            select(Event)
            .filter(Event.start_datetime > datetime.now(timezone.utc))
            .limit(event.limit)
            .offset(event.offset)
            .order_by(Event.created_at.desc())  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def _commit(self) -> None:
        await self._session.commit()

    async def get_events_by_addresses(self, addresses: list[UUID]) -> Sequence[Event]:
        """
        Получает все события по списку адресов.
        :param addresses: Список адресов.
        :return: Список событий.
        """

        query = select(Event).filter(Event.address_id.in_(addresses))
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()
