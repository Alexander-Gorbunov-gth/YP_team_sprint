from uuid import UUID

from pydantic import BaseModel, Field


class CreateBookmarkRequest(BaseModel):
    movie_uid: UUID = Field(..., description="ID фильма")


class CreateBookmarkResponse(BaseModel):
    id: str = Field(..., description="ID документа")
    movie_uid: UUID = Field(..., description="ID фильма")
    user_uid: UUID = Field(..., description="ID пользователя")
