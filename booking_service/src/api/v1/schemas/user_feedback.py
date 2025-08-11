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
    my: ReviewType | None = None


class ResultFeedbackResponseSchema(BaseModel):
    user_id: UUID
    my: str | None = None
    positive: int | None = None
    negative: int | None = None


class ResultUserEventFeedbackResponseSchema(BaseModel):
    user_id: UUID
    positive: int | None = None
    negative: int | None = None
