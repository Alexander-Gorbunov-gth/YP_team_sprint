from datetime import datetime

from src.domain.entities.address import Address
from src.domain.entities.event import Event
from src.domain.entities.user import User
from src.domain.entities.subscription import Subscription
from src.domain.entities.reservation import Reservation, ReservationStatus


address_data = Address(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05bb",
    country="Россия",
    city="Москва",
    street="Маяковская",
    house="15",
    flat="1"
)

reservation_data = Reservation(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05aa",
    user_id="2a736ae7-7c0f-429a-ba4b-f334e32d05ab",
    event_id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    seats=1,
    status=ReservationStatus.SUCCESS
)


event_data = Event(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    movie_id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    address_id="2a736ae7-7c0f-429a-ba4b-f334e32d05bb",
    address=address_data,
    owner_id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    reservations=[reservation_data, ],
    capacity=1,
    start_datetime=datetime.now()
)



sub_data = Subscription(
    host_id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    user_id="2a736ae7-7c0f-429a-ba4b-f334e32d05ab",
)