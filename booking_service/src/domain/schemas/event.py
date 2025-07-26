from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from .address import AdressRepresentSchema


class MovieSchema(BaseModel):
    genres: list[str]
    title: str
    description: str | None = None
    directors_names: list[str]
    actors_names: list[str]


class EventBaseSchema(BaseModel):
    movie_id: UUID
    address_id: UUID
    owner_id: UUID
    capacity: int
    start_datetime: datetime


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    movie_id: UUID | None

    address_id: UUID | None
    owner_id: UUID | None
    capacity: int | None
    start_datetime: datetime | None


class EventResponseSchema(EventBaseSchema):
    id: UUID
    address: AdressRepresentSchema
    movie: MovieSchema
