from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from src.domain.entities.reservation import Reservation, ReservationStatus
from src.domain.exceptions import DuplicateReservationError, EventUpdateLockedError, NotEnoughSeatsError
from tests.unit.factories import AddressFactory, EventFactory, UserFactory


@pytest.fixture
def address():
    return AddressFactory.build()


@pytest.fixture
def guest_user():
    return UserFactory.build()


@pytest.fixture
def host_user():
    return UserFactory.build()


@pytest.fixture
def event(address, host_user):
    return EventFactory.build(
        capacity=4,
        start_datetime=datetime.now() + timedelta(hours=1),
        addres=address,
        address_id=address.id,
        owner_id=host_user.id,
        reservations=[],
    )


def test_successful_reservation(event, guest_user):
    reservation = event.reserve(user_id=guest_user.id, seats_requested=2)
    event.add_reservasion(reservation)

    assert isinstance(reservation, Reservation)
    assert reservation.user_id == guest_user.id
    assert reservation.status == ReservationStatus.PENDING
    assert event.capacity - 2 == event.available_seats()


def test_user_cannot_reserve_twice(event, guest_user):
    reservation = event.reserve(user_id=guest_user.id, seats_requested=1)
    event.add_reservasion(reservation)

    with pytest.raises(DuplicateReservationError):
        reservation_2 = event.reserve(user_id=guest_user.id, seats_requested=1)
        event.add_reservasion(reservation_2)

    assert len(event.reservations) == 1


def test_cannot_reserve_more_than_available(event, guest_user):
    reservation = event.reserve(user_id=guest_user.id, seats_requested=3)
    event.add_reservasion(reservation)

    assert reservation.status == ReservationStatus.PENDING
    assert event.capacity - 3 == event.available_seats()

    random_uuid = uuid4()

    with pytest.raises(NotEnoughSeatsError):
        reservation_2 = event.reserve(user_id=random_uuid, seats_requested=2)
        event.add_reservasion(reservation_2)

    assert len(event.reservations) == 1


def test_cannot_update_event(event):
    random_address_uuid = uuid4()
    with pytest.raises(EventUpdateLockedError):
        event.change_address(new_address_id=random_address_uuid)

    with pytest.raises(EventUpdateLockedError):
        event.change_datetime(datetime.now())
