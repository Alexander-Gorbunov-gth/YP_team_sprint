
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

        
class ShortFilm(BaseModel):
    id:str
    title:str
    imdb_rating:float

class FilmRole(BaseModel):
    id: str
    roles: List[str]

class Person(BaseModel):
    id:str
    full_name:str
    films:List[FilmRole]

class EntityBase(BaseModel):
    id: str
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
    id: str
    title: str
    imdb_rating: Optional[float]
    description:Optional[str]
    genres:List[str]
    actors:List[Actor]
    writers:List[Writer]
    directors:List[Director]
    
    
