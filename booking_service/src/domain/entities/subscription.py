from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.mixins import DateTimeMixin


class Subscription(DateTimeMixin, BaseModel):
    id: int
    host_id: UUID
    user_id: UUID

    @classmethod
    def create(cls,id: int, host_id: UUID, user_id: UUID) -> "Subscription":
        return cls(id=id, host_id=host_id, user_id=user_id)
