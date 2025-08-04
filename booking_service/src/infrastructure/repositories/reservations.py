import logging
from uuid import UUID

from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.reservation import Reservation
from src.infrastructure.repositories.exceptions import ReservationNotFoundError
from src.services.interfaces.repositories.reservation import IReservationRepository

logger = logging.getLogger(__name__)


class SQLAlchemyReservationRepository(IReservationRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, reservation: Reservation) -> Reservation:
        """
        Создает бронирование в базе данных.
        :param reservation: Схема бронирования для создания.
        :return: Созданное бронирование.
        """

        query = insert(Reservation).values(reservation.model_dump()).returning(Reservation)
        created_subscription: Result = await self._session.execute(query)
        await self._commit()
        return created_subscription.scalar_one()

    async def update(self, reservation_id: UUID | str, reservation: Reservation) -> Reservation | None:
        """
        Обновляет бронирование в базе данных.
        :param reservation: Обновлённый объект бронирования.
        :raises ReservationNotFoundError: Если бронирование не найдено.
        :return: Обновлённое бронирование.
        """

        query = select(Reservation).filter_by(id=reservation_id)
        result: Result = await self._session.execute(query)
        existing_reservation: Reservation | None = result.scalar_one_or_none()

        if existing_reservation is None:
            raise ReservationNotFoundError(f"Бронирование с {reservation_id=} не найдено.")

        update_data = reservation.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in update_data.items():
            setattr(existing_reservation, field, value)

        self._session.add(existing_reservation)
        await self._commit()
        await self._session.refresh(existing_reservation)

        return existing_reservation

    async def delete(self, reservation_id: UUID | str) -> None:
        """
        Удаляет бронирование из базы данных.
        :param reservation_id: ID бронирования в базе данных.
        :raises ReservationNotFoundError: Если бронирование не найдено.
        """

        check_query = select(Reservation).filter_by(id=reservation_id)
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()

        if existing is None:
            raise ReservationNotFoundError(f"Бронирование с {reservation_id=} не найдена.")

        await self._session.delete(existing)
        await self._commit()

    async def get_by_id(self, reservation_id: UUID | str) -> Reservation | None:
        """
        Получает одно бронирование по ID.
        :param reservation_id: ID бронирования.
        :return: Модель бронирования.
        """

        query = select(Reservation).filter_by(id=reservation_id)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID | str) -> list[Reservation]:
        """
        Получает все брони пользователя.
        :param user_id: ID пользователя.
        :return: Список броней.
        """

        query = (
            select(Reservation).filter_by(user_id=user_id).order_by(Reservation.created_at.desc())  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.scalars().all()

    async def _commit(self) -> None:
        await self._session.commit()
