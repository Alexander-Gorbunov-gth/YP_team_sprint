from uuid import UUID, uuid4

from pydantic import BaseModel

from src.domain.entities.mixins import DateTimeMixin


class Subscription(DateTimeMixin, BaseModel):
    id: UUID
    host_id: UUID
    user_id: UUID

    @classmethod
    def create(cls, host_id: UUID, user_id: UUID) -> "Subscription":
        return cls(id=uuid4(), host_id=host_id, user_id=user_id)
