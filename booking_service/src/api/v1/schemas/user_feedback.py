from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class UserFeedbackBaseSchema(BaseModel):
    user_id: UUID
    review: ReviewType


class UserFeedbackCreateSchema(UserFeedbackBaseSchema):
    pass


class UserFeedbackResponseSchema(UserFeedbackBaseSchema):
    id: UUID
    owner_id: UUID
