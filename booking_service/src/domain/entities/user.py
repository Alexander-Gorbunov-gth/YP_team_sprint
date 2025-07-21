from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID

    @classmethod
    def create(cls, user_id: UUID) -> "User":
        return cls(id=user_id)
