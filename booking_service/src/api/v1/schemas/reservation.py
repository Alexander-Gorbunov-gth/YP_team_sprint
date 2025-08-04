from uuid import UUID

from pydantic import BaseModel

from src.api.v1.schemas.utils import MovieSchema
from src.domain.entities.reservation import ReservationStatus


class ReservationBaseSchema(BaseModel):
    event_id: UUID
    seats: int
    status: ReservationStatus


class ReservationUpdateSchema(BaseModel):
    seats: int | None = None
    status: ReservationStatus | None = None


class ReservationCreateSchema(BaseModel):
    event_id: UUID
    seats: int


class ReservationResponseSchema(BaseModel):
    id: UUID
    event_id: UUID
    seats: int
    status: ReservationStatus
