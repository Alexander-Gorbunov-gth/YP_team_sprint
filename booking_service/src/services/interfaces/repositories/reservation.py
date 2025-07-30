import abc
from uuid import UUID

from src.api.v1.schemas.reservation import ReservationCreateSchema, ReservationUpdateSchema
from src.domain.entities.reservation import Reservation


class IReservationRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, reservation: ReservationCreateSchema) -> Reservation: ...

    @abc.abstractmethod
    async def update(self, reservation_id: UUID | str, reservation: ReservationUpdateSchema) -> Reservation | None: ...

    @abc.abstractmethod
    async def delete(self, reservation_id: UUID | str) -> None: ...

    @abc.abstractmethod
    async def get_by_id(self, reservation_id: UUID | str) -> Reservation | None: ...

    @abc.abstractmethod
    async def get_by_user_id(self, user_id: UUID | str) -> list[Reservation]: ...
