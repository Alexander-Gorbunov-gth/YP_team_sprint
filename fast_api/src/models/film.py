
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from typing import List, Optional
from pydantic import BaseModel


class Person(BaseModel):
    uuid:str
    name:str
    
class Actor(Person):
    pass

class Writer(Person):
    pass

class Director(Person):
    pass

class Genre(BaseModel):
    uuid:str
    name:str
    
class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]
    description:Optional[str]
    genre:List[Genre]
    actors:List[Actor]
    writers:List[Writer]
    directors:List[Director]
    
    
