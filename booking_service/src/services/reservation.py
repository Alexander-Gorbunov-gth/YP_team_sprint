import abc
from uuid import UUID

from src.api.v1.schemas.reservation import ReservationCreateSchema, ReservationUpdateSchema
from src.core.config import settings
from src.domain.entities.event import Reservation, ReservationStatus
from src.services.exceptions import ReservationNotFoundError
from src.services.interfaces.producer import PublishMessage
from src.services.interfaces.uow import IUnitOfWork


class IReservationService(abc.ABC):
    @abc.abstractmethod
    async def create(self, reservation: ReservationCreateSchema) -> Reservation | None: ...

    @abc.abstractmethod
    async def update(self, reservation_id: UUID | str, reservation: ReservationUpdateSchema) -> Reservation | None: ...

    @abc.abstractmethod
    async def delete(self, reservation_id: UUID | str) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, reservation_id: UUID | str) -> Reservation: ...

    @abc.abstractmethod
    async def get_by_user_id(self, user_id: UUID | str) -> list[Reservation]: ...


class ReservationService(IReservationService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def create(self, reservation: ReservationCreateSchema) -> Reservation | None:
        async with self._uow as uow:
            await uow.producer.publish(
                message=PublishMessage(
                    event_type="send_notification",
                    channels=["email"],
                    user_params={
                        "body": "Пользователь создал бронь",
                        "subject": "Примите или отклоните его заявку.",
                        "address": "",  # TODO: Получить email организатора.
                        "user_uuid": (await uow.event_repository.get_by_id(reservation.event_id)).owner_id,
                    },
                ),
                routing_key=settings.rabbit.email_queue_title,
            )
            return await uow.reservation_repository.create(reservation)

    async def update(self, reservation_id: UUID | str, reservation: ReservationUpdateSchema) -> Reservation | None:
        async with self._uow as uow:
            current_reservation = await uow.reservation_repository.get_by_id(reservation_id)
            if current_reservation is None:
                raise ReservationNotFoundError("Reservation not found")

            if current_reservation.status != reservation.status:
                messages = {
                    ReservationStatus.SUCCESS: "Ваша бронь принята.",
                    ReservationStatus.CANCELED: "Ваша бронь отклонена.",
                }
                notification_message = PublishMessage(
                    event_type="send_notification",
                    channels=["email"],
                    user_params={
                        "body": messages.get(reservation.status),
                        "subject": "Организатор принял решение по вашей заявке",
                        "address": "",  # TODO: Получить email пользователя.
                        "user_uuid": (await uow.event_repository.get_by_id(current_reservation.event_id)).owner_id,
                    },
                )
                await uow.producer.publish(message=notification_message, routing_key=settings.rabbit.email_queue_title)

            return await uow.reservation_repository.update(reservation_id, reservation)

    async def delete(self, reservation_id: UUID | str) -> None:
        async with self._uow as uow:
            current_reservation = await uow.reservation_repository.get_by_id(reservation_id)
            if current_reservation is None:
                raise ReservationNotFoundError("Reservation not found")
            # Сообщить модеру, что бронь снята
            await uow.producer.publish(
                message=PublishMessage(
                    event_type="send_notification",
                    channels=["email"],
                    user_params={
                        "body": "Пользователь отменил бронь",
                        "subject": "Пользователь отменил бронь.",
                        "address": "",  # TODO: Получить email организатора.
                        "user_uuid": (await uow.event_repository.get_by_id(current_reservation.event_id)).owner_id,
                    },
                ),
                routing_key=settings.rabbit.email_queue_title,
            )
            await uow.reservation_repository.delete(reservation_id)

    async def get_by_id(self, reservation_id: UUID | str) -> Reservation:
        async with self._uow as uow:
            current_reservation = await uow.reservation_repository.get_by_id(reservation_id)
            if current_reservation is None:
                raise ReservationNotFoundError("Reservation not found")
            return current_reservation

    async def get_by_user_id(self, user_id: UUID | str) -> list[Reservation]:
        async with self._uow as uow:
            current_reservations = await uow.reservation_repository.get_by_user_id(user_id)
            if not current_reservations:
                raise ReservationNotFoundError("Reservations not found")
            return current_reservations
