from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.mixins import DateTimeMixin


class Subscription(DateTimeMixin, BaseModel):
    host_id: UUID
    user_id: UUID

    @classmethod
    def create(cls, host_id: UUID, user_id: UUID) -> "Subscription":
        return cls(host_id=host_id, user_id=user_id)
