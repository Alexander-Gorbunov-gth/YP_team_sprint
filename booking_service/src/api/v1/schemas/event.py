from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.api.v1.schemas.address import AddressResponseSchema
from src.api.v1.schemas.utils import Author, MovieSchema


class EventBaseSchema(BaseModel):
    movie_id: UUID
    address_id: UUID
    owner_id: UUID
    capacity: int
    start_datetime: datetime


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    # movie_id: UUID | None - сам фильм запретим менять
    address_id: UUID | None
    # owner_id: UUID | None - # сам автор запретим менять
    capacity: int | None
    start_datetime: datetime | None


class EventResponseSchema(EventBaseSchema):
    id: UUID
    address: AddressResponseSchema
    movie: MovieSchema
    author: Author


class EventMyResponseSchema(EventResponseSchema):
    customers: list
