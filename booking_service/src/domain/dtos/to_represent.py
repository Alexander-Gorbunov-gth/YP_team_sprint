from uuid import UUID

from pydantic import BaseModel


class Author(BaseModel):
    id: UUID
    name: str
    username: str


class MovieSchema(BaseModel):
    genres: list[str]
    title: str
    description: str | None = None
    directors_names: list[str]
    actors_names: list[str]
