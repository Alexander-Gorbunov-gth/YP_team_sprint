from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.reservation import ReservationStatus

from .event import MovieSchema


class ReservationBaseSchema(BaseModel):
    # user_id: UUID - забрать из токена
    event_id: UUID
    seats: int
    status: ReservationStatus


class ReservationCreateSchema(ReservationBaseSchema):
    pass


class ReservationRepresentSchema(ReservationBaseSchema):
    id: UUID
    movie: MovieSchema


class ReservationUpdateSchema(BaseModel):
    seats: int | None = None
    status: ReservationStatus | None = None
