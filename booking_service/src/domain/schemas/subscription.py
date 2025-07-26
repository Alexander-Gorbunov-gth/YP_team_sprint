from uuid import UUID

from pydantic import BaseModel

from src.domain.schemas.to_represent import Author


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
