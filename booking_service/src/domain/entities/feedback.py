from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.mixins import DateTimeMixin


class ReviewType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class EventFeedbackBaseSchema(DateTimeMixin, BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    review: ReviewType


class EventFeedback(EventFeedbackBaseSchema):
    event_id: UUID


class UserFeedback(EventFeedbackBaseSchema):
    owner_id: UUID
