from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.domain.schemas.to_represent import Author


class BaseSubscriptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    host_id: UUID
    # user_id: UUID


class SubscriptionCreateSchema(BaseSubscriptionSchema):
    pass


class SubscriptionDeleteSchema(BaseSubscriptionSchema):
    pass


class SubscriptionRepresentSchema(BaseSubscriptionSchema):
    pass
    author: Author
