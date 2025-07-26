from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.reservation import ReservationStatus


class ReservationBaseSchema(BaseModel):
    # user_id: UUID - забрать из токена
    event_id: UUID
    seats: int
    status: ReservationStatus


class ReservationCreateSchema(ReservationBaseSchema):
    pass


class ReservationRepresentSchema(ReservationBaseSchema):
    id: UUID


class ReservationUpdateSchema(BaseModel):
    seats: int | None
    status: ReservationStatus | None
