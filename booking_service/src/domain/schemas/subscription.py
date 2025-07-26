from uuid import UUID

from pydantic import BaseModel


class BaseSubscriptionSchema(BaseModel):
    host_id: UUID
    user_id: UUID


class SubscriptionCreateSchema(BaseSubscriptionSchema):
    pass


class SubscriptionDeleteSchema(BaseSubscriptionSchema):
    pass


class SubscriptionRepresentSchema(BaseSubscriptionSchema):
    pass
