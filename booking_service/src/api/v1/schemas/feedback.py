from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class FeedbackBaseSchema(BaseModel):
    event_id: UUID
    review: ReviewType


class FeedbackCreateSchema(FeedbackBaseSchema):
    pass


class FeedbackResponseSchema(FeedbackBaseSchema):
    id: UUID
    user_id: UUID
