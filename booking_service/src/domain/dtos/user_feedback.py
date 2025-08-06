from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.feedback import ReviewType


class UserFeedbackBaseSchema(BaseModel):
    user_id: UUID
    owner_id: UUID


class UserFeedbackCreateDTO(UserFeedbackBaseSchema):
    review: ReviewType


class UserFeedbackUpdateDTO(UserFeedbackBaseSchema):
    review: ReviewType


class UserFeedbackDeleteDTO(UserFeedbackBaseSchema):
    pass
