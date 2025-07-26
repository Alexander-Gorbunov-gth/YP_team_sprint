from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.mixins import DateTimeMixin


class ReservationStatus(Enum):
    PENDING = "pending"
    CANCELED = "canceled"
    SUCCESS = "success"


class Reservation(DateTimeMixin, BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_id: UUID
    seats: int = Field(ge=1, le=10)
    status: ReservationStatus = Field(default=ReservationStatus.PENDING)

    @classmethod
    def create(cls, user_id: UUID, event_id: UUID, seats: int) -> "Reservation":
        return cls(
            user_id=user_id,
            event_id=event_id,
            seats=seats,
            status=ReservationStatus.PENDING,
        )

    def approve_reservation(self) -> None:
        self.status = ReservationStatus.SUCCESS
        self.touch()

    def cancel_reservation(self) -> None:
        self.status = ReservationStatus.CANCELED
        self.touch()
