from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class EventFeedbackBaseSchema(BaseModel):
    event_id: UUID
    user_id: UUID


class EventFeedbackCreateDTO(EventFeedbackBaseSchema):
    review: ReviewType


class EventFeedbackUpdateDTO(EventFeedbackBaseSchema):
    review: ReviewType


class EventFeedbackDeleteDTO(EventFeedbackBaseSchema):
    pass
