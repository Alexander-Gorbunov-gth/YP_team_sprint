from datetime import datetime

from src.domain.entities.address import Address
from src.domain.entities.event import Event
from src.domain.entities.reservation import Reservation, ReservationStatus
from src.domain.entities.subscription import Subscription
from src.api.v1.schemas.utils import Author, MovieSchema
from src.api.v1.schemas.event import EventResponseSchema
from src.api.v1.schemas.reservation import ReservationResponseSchema
from src.api.v1.schemas.subscription import SubscriptionResponseSchema
from src.api.v1.schemas.address import AddressResponseSchema

address_data = AddressResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05bb",
    country="Россия",
    city="Москва",
    street="Маяковская",
    house="15",
    flat="1",
)


author_data = Author(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    name="John Doe",
    username="john.doe@example.com",
)

movie_data = MovieSchema(
    genres=["Drama", "Action"],
    title="Epic Movie",
    description="An epic movie about heroes.",
    directors_names=["Jane Smith"],
    actors_names=["John Doe", "Jane Doe"],
)

reservation_data = ReservationResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05aa",
    user_id="2a736ae7-7c0f-429a-ba4b-f334e32d05ab",
    event_id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    seats=1,
    status=ReservationStatus.PENDING,
    movie=movie_data,
)

movie_event_data = MovieSchema(
    id="2a736ae7-7c0f-429a-ba4b-ba4b-f334e32d05cc",
    genres=["Drama", "Action"],
    title="Фильм",
    description="An epic movie about heroes.",
    directors_names=["Jane Smith"],
    actors_names=["John Doe", "Jane Doe"],
)

event_data = EventResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    movie_id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    address_id="2a736ae7-7c0f-429a-ba4b-f334e32d05bb",
    address=address_data.model_dump(),
    owner_id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    reservations=[
        reservation_data,
    ],
    capacity=1,
    start_datetime=datetime.now(),
    movie=movie_data,
    author=author_data,
)

event_my_data = EventResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    movie_id="2a736ae7-7c0f-429a-ba4b-f334e32d05cc",
    address_id="2a736ae7-7c0f-429a-ba4b-f334e32d05bb",
    address=address_data.model_dump(),
    owner_id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    reservations=[
        reservation_data,
    ],
    capacity=1,
    start_datetime=datetime.now(),
    movie=movie_event_data,
    author=author_data,
)


sub_data1 = SubscriptionResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05aa",
    host_id="2a736ae7-7c0f-429a-ba4b-f334e32d0aaa",
    user_id="2a736ae7-7c0f-429a-ba4b-f334e32d05ab",
    author=author_data,
)
sub_data2 = SubscriptionResponseSchema(
    id="2a736ae7-7c0f-429a-ba4b-f334e32d05ab",
    host_id="2a736ae7-7c0f-429a-ba4b-f334e32d0bbb",
    user_id="2a736ae7-7c0f-429a-ba4b-f334e32d0bbb",
    author=author_data,
)
