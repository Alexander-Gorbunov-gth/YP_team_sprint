from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: float
    genres: list[str]
    title: str
    description: str | None = None
    directors_names: str
    actors_names: str
    writers_names: str
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]


class ResponseFilm(BaseModel):
    id: str
    imdb_rating: float
    genres: list[str]
    title: str
    description: str | None = None
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
