from uuid import UUID

from pydantic import BaseModel

from src.api.v1.schemas.utils import Author


class SubscriptionCreateSchema(BaseModel):
    host_id: UUID


class SubscriptionDeleteSchema(BaseModel):
    host_id: UUID


class SubscriptionResponseSchema(BaseModel):
    user_id: UUID
    host_id: UUID
    author: Author
