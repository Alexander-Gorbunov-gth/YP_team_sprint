from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventCreateSchema(BaseModel):
    movie_id: UUID
    address_id: UUID
    owner_id: UUID
    capacity: int
    start_datetime: datetime


class EventUpdateSchema(BaseModel):
    id: UUID
    movie_id: UUID | None
    address_id: UUID | None
    owner_id: UUID | None
    capacity: int | None
    start_datetime: datetime | None


class EventReadSchema(BaseModel):
    pass
