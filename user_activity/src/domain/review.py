from uuid import UUID

from pydantic import Field
from src.domain.base import TimestampMixin


class Review(TimestampMixin):
    movie_id: UUID = Field(..., description="ID фильма")
    user_id: UUID = Field(..., description="ID пользователя")
    rating: int = Field(..., ge=1, le=10, description="Оценка фильма (1–10)")
    content: str = Field(..., description="Тело рецензии")

    @classmethod
    def create(cls, movie_id: UUID, user_id: UUID, rating: int, content: str) -> "Review":
        return cls(movie_id=movie_id, user_id=user_id, rating=rating, content=content.strip())
