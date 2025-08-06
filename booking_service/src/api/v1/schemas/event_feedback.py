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
