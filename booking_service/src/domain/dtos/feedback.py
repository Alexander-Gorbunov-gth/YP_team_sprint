from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class FeedbackBaseSchema(BaseModel):
    event_id: UUID
    user_id: UUID


class FeedbackCreateDTO(FeedbackBaseSchema):
    review: ReviewType


class FeedbackUpdateDTO(FeedbackBaseSchema):
    review: ReviewType


class FeedbackDeleteDTO(FeedbackBaseSchema):
    pass
