from uuid import UUID

from pydantic import Field
from src.domain.base import TimestampMixin


class Like(TimestampMixin):
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")

    @classmethod
    def create(cls, movie_id: UUID, user_id: UUID) -> "Like":
        return cls(movie_id=movie_id, user_id=user_id)
