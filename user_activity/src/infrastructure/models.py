from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class LikeModel(Document, TimestampMixin):
    movie_uid: UUID
    user_uid: UUID

    class Settings:
        name = "like"


class BookmarkModel(Document, TimestampMixin):
    movie_uid: UUID
    user_uid: UUID

    class Settings:
        name = "bookmark"


class ReviewModel(Document, TimestampMixin):
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")
    rating: int = Field(..., ge=1, le=10, description="Оценка фильма (1–10)")
    content: str = Field(..., description="Тело рецензии")

    class Settings:
        name = "review"
