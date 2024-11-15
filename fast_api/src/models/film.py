
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class FilmRole(BaseModel):
    id: UUID
    roles: List[str]

class Person(BaseModel):
    id:UUID
    full_name:str
    films:List[FilmRole]

class EntityBase(BaseModel):
    id: UUID
    name: str
class Actor(EntityBase):
    pass
class Writer(EntityBase):
    pass
class Director(EntityBase):
    pass
class Genre(EntityBase):
    pass
    
class Film(BaseModel):
    id: UUID
    title: str
    imdb_rating: Optional[float]
    description:Optional[str]
    genre:List[Genre]
    actors:List[Actor]
    writers:List[Writer]
    directors:List[Director]
    
    
