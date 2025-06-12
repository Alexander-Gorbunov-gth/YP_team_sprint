from uuid import UUID

from pydantic import Field
from src.domain.base import TimestampMixin


class Review(TimestampMixin):
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")
    rating: int = Field(..., ge=1, le=10, description="Оценка фильма (1–10)")
    content: str = Field(..., description="Тело рецензии")

    @classmethod
    def create(cls, movie_uid: UUID, user_uid: UUID, rating: int, content: str) -> "Review":
        return cls(movie_uid=movie_uid, user_uid=user_uid, rating=rating, content=content.strip())
