from http import HTTPStatus
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from pydantic import BaseModel

from src.services.film import FilmService, get_film_service
from src.models.person import Person, ShortFilm
from src.services.persons import PersonService, get_person_service

logger = logging.getLogger(__name__)

router = APIRouter()


# поиск по персонам с возможностью передачи query параметров 
@router.get('/search', response_model=list[Person])
@cache(expire=60)
async def all_persons(person_service: PersonService = Depends(get_person_service),
                      name: str | None = Query(None, alias="name"),
                      order: str = Query("asc", enum=["asc", "desc"]),
                      limit: int = Query(10, gt=0, le=100),
                      offset: int = Query(0, ge=0)
                      ) -> list[Person] | None:
    try:
        persons = await person_service.get_all_persons(query, order, page_size, page_number)
        if not persons:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Персоны не найдены")
        return persons
    except Exception as e:
        logger.error(f"Ошибка при получении персон: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                            detail=f"Ошибка при получении персон: {str(e)}")


@router.get('/{person_id}/film', response_model=list[ShortFilm])
@cache(expire=60)
async def films_by_person(person_id: str,
                          person_service: PersonService = Depends(get_person_service),
                          film_service: FilmService = Depends(get_film_service)) -> list[ShortFilm]:
    films_id = []
    films = []
    try:
        person = await person_service.get_by_id(person_id)
        if not person:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Персона не найдена')
        for film in person.films:
            films_id.append(film.id)

        for id in films_id:
            film = await film_service.get_by_id(str(id))
            short_film = {"id": film.model_dump()['id'], "title": film.model_dump()['title'],
                          "imdb_rating": film.model_dump()['imdb_rating']}
            films.append(ShortFilm(**short_film))

        return films

    except Exception as e:
        logger.error(f"Ошибка при поиске фильмов по персоне с ID {person_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка сервера")


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
        logger.error(f"Ошибка при поиске персоны по ID {person_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Ошибка сервера")
