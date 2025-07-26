from uuid import UUID

from pydantic import BaseModel


class Author(BaseModel):
    id: UUID
    name: str
    username: str


class BaseSubscriptionSchema(BaseModel):
    host_id: UUID
    # user_id: UUID - забрать из токена


class SubscriptionCreateSchema(BaseSubscriptionSchema):
    pass


class SubscriptionDeleteSchema(BaseSubscriptionSchema):
    pass


class SubscriptionRepresentSchema(BaseSubscriptionSchema):
    pass
    author: Author
