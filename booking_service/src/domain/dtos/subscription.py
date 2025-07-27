from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubscriptionBaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    host_id: UUID
    user_id: UUID


class SubscriptionCreateDTO(SubscriptionBaseDTO):
    pass


class SubscriptionDeleteDTO(SubscriptionBaseDTO):
    pass
