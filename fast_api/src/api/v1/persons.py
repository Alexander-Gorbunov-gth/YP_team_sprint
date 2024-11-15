from http import HTTPStatus
from typing import List, Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from src.models.film import Genre, Person
from src.services.persons import PersonService, get_person_service


logger = logging.getLogger(__name__)

router = APIRouter()

# поиск по персонам по id
@router.get('/{person_id}', response_model=Person)
@cache(expire=60)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    try:
        person = await person_service.get_by_id(person_id)
        
        if not person:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Персона не найдена')
        
        return Person(id=person.id, full_name=person.full_name, films=person.films)
    
    except Exception as e:
        print(f"Ошибка при поиске персоны по ID {person_id}: {str(e)}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка сервера")

# поиск по персонам с возможностью передачи query параметров 
@router.get('/', response_model=List[Person])
@cache(expire=60)
async def all_persons(person_service: PersonService = Depends(get_person_service),
                        name: Optional[str] = Query(None, alias="name"),
                        order: str = Query("asc", enum=["asc", "desc"]),
                        limit: int = Query(10, gt=0, le=100),
                        offset: int = Query(0, ge=0)
                      )->Optional[List[Person]]:
    try:
        persons = await person_service.get_all_persons(name, order, limit, offset)
        if not persons:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Персоны не найдены")
        return persons    
    except Exception as e:
        logger.error(f"Ошибка при получении персон: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Ошибка при получении персон: {str(e)}")
        





