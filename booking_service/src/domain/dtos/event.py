from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventCreateDTO(BaseModel):
    movie_id: UUID
    address_id: UUID
    # owner_id: UUID - забрать из токена
    capacity: int
    start_datetime: datetime


class EventUpdateDTO(BaseModel):
    id: UUID
    movie_id: UUID | None = None
    address_id: UUID | None = None
    capacity: int | None = None
    start_datetime: datetime | None = None
