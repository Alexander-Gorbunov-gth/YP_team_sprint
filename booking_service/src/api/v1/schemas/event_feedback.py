from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class EventFeedbackBaseSchema(BaseModel):
    event_id: UUID
    review: ReviewType


class EventFeedbackCreateSchema(EventFeedbackBaseSchema):
    pass


class EventFeedbackResponseSchema(EventFeedbackBaseSchema):
    id: UUID
    user_id: UUID


class ResultEventFeedbackResponseSchema(BaseModel):
    user_id: UUID
    my: str | None = None
    positive: int | None = None
    negative: int | None = None
