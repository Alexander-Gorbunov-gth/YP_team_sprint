from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Author(BaseModel):
    id: UUID
    name: str
    username: str


class BaseSubscriptionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    host_id: UUID
    user_id: UUID


class SubscriptionCreateSchema(BaseSubscriptionSchema):
    pass


class SubscriptionDeleteSchema(BaseSubscriptionSchema):
    pass


class SubscriptionRepresentSchema(BaseSubscriptionSchema):
    pass
    author: Author
