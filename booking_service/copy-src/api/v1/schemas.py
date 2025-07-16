from uuid import UUID

from pydantic import BaseModel, Field


class CreateBookmarkRequest(BaseModel):
    movie_uid: UUID = Field(..., description="ID фильма")


class BookmarkResponse(BaseModel):
    id: str = Field(..., description="ID документа")
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")


class CreateLikeRequest(BaseModel):
    movie_uid: UUID = Field(..., description="ID фильма")


class LikeResponse(BaseModel):
    id: str = Field(..., description="ID документа")
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")


class LikeCountResponse(BaseModel):
    count: int = Field(..., description="Количество лайков")
    movie_uid: UUID = Field(..., description="ID фильма")


class CreateReviewRequest(BaseModel):
    movie_uid: UUID = Field(..., description="ID фильма")
    rating: int = Field(..., description="Рейтинг", ge=1, le=10)
    content: str = Field(..., description="Контент", min_length=1, max_length=1000)


class ReviewResponse(BaseModel):
    id: str = Field(..., description="ID документа")
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")
    rating: int = Field(..., description="Рейтинг", ge=1, le=10)
    content: str = Field(..., description="Контент", min_length=1, max_length=1000)


class ReviewCountResponse(BaseModel):
    count: int = Field(..., description="Количество рецензий")
    movie_uid: UUID = Field(..., description="ID фильма")


class ReviewAverageResponse(BaseModel):
    average: float = Field(..., description="Средний рейтинг", ge=1, le=10)
    movie_uid: UUID = Field(..., description="ID фильма")


class UpdateReviewRequest(BaseModel):
    rating: int | None = Field(default=None, description="Рейтинг", ge=1, le=10)
    content: str | None = Field(default=None, description="Контент", min_length=1, max_length=1000)
