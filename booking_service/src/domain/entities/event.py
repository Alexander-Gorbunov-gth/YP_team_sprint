from datetime import datetime, timedelta
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.address import Address
from src.domain.entities.mixins import DateTimeMixin
from src.domain.entities.reservation import Reservation, ReservationStatus
from src.domain.exceptions import DuplicateReservationError, EventUpdateLockedError, NotEnoughSeatsError


class Event(DateTimeMixin, BaseModel):
    id: UUID = Field(default_factory=uuid4)
    movie_id: UUID
    address_id: UUID
    address: Address | None = Field(default=None)
    owner_id: UUID
    reservations: list[Reservation] = Field(default_factory=list)
    capacity: int = Field(ge=1, le=100)
    start_datetime: datetime

    UPDATE_LOCK_TIMEDELTA: timedelta = Field(timedelta(hours=2))

    @classmethod
    def create(
        cls, movie_id: UUID, address_id: UUID, owner_id: UUID, capacity: int, start_datetime: datetime
    ) -> "Event":
        return cls(
            movie_id=movie_id,
            address_id=address_id,
            owner_id=owner_id,
            capacity=capacity,
            start_datetime=start_datetime,
        )

    def available_seats(self) -> int:
        reserved = sum(
            r.seats for r in self.reservations if r.status in {ReservationStatus.PENDING, ReservationStatus.SUCCESS}
        )
        return self.capacity - reserved

    def has_reservation_for(self, user_id: UUID) -> bool:
        return any(r.user_id == user_id for r in self.reservations)

    def can_reserve_seats(self, seats_requested: int) -> bool:
        return seats_requested <= self.available_seats()

    def add_reservasion(self, reservation: Reservation) -> None:
        self.reservations.append(reservation)
        self.touch()

    def cancel_reservation(self, reservation: Reservation) -> None:
        self.reservations.remove(reservation)
        self.touch()

    def reserve(self, user_id: UUID, seats_requested: int) -> Reservation:
        if not self.can_reserve_seats(seats_requested=seats_requested):
            raise NotEnoughSeatsError

        if self.has_reservation_for(user_id=user_id):
            raise DuplicateReservationError

        reservation = Reservation.create(user_id=user_id, event_id=self.id, seats=seats_requested)
        self.reservations.append(reservation)
        return reservation

    def can_be_updated(self) -> bool:
        now = datetime.now()
        if (self.start_datetime - now) < self.UPDATE_LOCK_TIMEDELTA:
            raise EventUpdateLockedError
        return True

    def change_datetime(self, new_start_datetime: datetime):
        if self.can_be_updated():
            self.start_datetime = new_start_datetime
            self.touch()

    def change_address(self, new_address_id: UUID):
        if self.can_be_updated():
            self.address_id = new_address_id
            self.touch()
