from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Author(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default="John Doe")
    username: str = Field(default="john_doe")


class MovieSchema(BaseModel):
    genres: list[str] = Field(default_factory=list)
    title: str = Field(default="Movie Title")
    description: str | None = None
    directors_names: list[str] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
