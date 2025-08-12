from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.v1.schemas.address import AddressResponseSchema
from src.api.v1.schemas.utils import Author, MovieSchema
from src.api.v1.schemas.reservation import ReservationResponseSchema


class EventBaseSchema(BaseModel):
    movie_id: UUID
    address_id: UUID
    capacity: int
    start_datetime: datetime


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    address_id: UUID | None = Field(default=None)
    capacity: int | None = Field(default=None)
    start_datetime: datetime | None = Field(default=None)


class EventResponseSchema(EventBaseSchema):
    id: UUID
    address: str
    available_seats: int
    movie: MovieSchema
    author: Author
    reservations: list[ReservationResponseSchema] = Field(default_factory=list)


class EventMyResponseSchema(EventResponseSchema):
    customers: list


class EventGetAllSchema(BaseModel):
    offset: int
    limit: int


class GetNearbyEventsSchema(BaseModel):
    address: UUID
    radius: float = Field(
        default=5.0, description="Радиус в километрах (по умолчанию 5 км)"
    )
