from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class LikesModel(Document, TimestampMixin):
    movie_uuid: UUID
    user_uuid: UUID

    class Settings:
        name = "likes"


class BookmarksModel(Document, TimestampMixin):
    movie_uuid: UUID
    user_uuid: UUID

    class Settings:
        name = "bookmarks"


class ReviewsModel(Document, TimestampMixin):
    movie_id: UUID = Field(..., description="ID фильма")
    user_id: UUID = Field(..., description="ID пользователя")
    rating: int = Field(..., ge=1, le=10, description="Оценка фильма (1–10)")
    content: str = Field(..., description="Тело рецензии")

    class Settings:
        name = "reviews"
