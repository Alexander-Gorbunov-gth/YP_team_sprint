"""Эндпоинты для работы с персонами"""

import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from src.core.auth import require_permissions
from src.core.permissions import permissions
from src.models.person import Person, ShortFilm
from src.services.film import FilmService, get_film_service
from src.services.persons import PersonService, get_person_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=list[Person])
async def person_list(
    person_service: PersonService = Depends(get_person_service),
    page_size: int = Query(10, gt=0, le=100),
    page: int = Query(1, ge=1),
    perm: bool = Depends(require_permissions([permissions.persons_can_view])),
) -> list[Person] | None:
    """Получает постраничный список персон"""

    persons = await person_service.get_person_list(
        page_size=page_size, page=page
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Ошибка при получении персон",
        )
    return persons


@router.get("/search/", response_model=list[Person])
async def person_search(
    query: str = Query(..., alias="query"),
    page_size: int = Query(default=10, gt=1, le=50, alias="page_size"),
    page: int = Query(default=1, ge=1, alias="page"),
    person_service: PersonService = Depends(get_person_service),
    perm: bool = Depends(require_permissions([permissions.persons_can_view])),
):
    """Получает список персон по поисковому запросу"""

    search_fields = ["full_name"]
    print(query)
    persons = await person_service.get_person_by_query(
        query=query,
        search_fields=search_fields,
        page_size=page_size,
        page=page,
    )
    if persons is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Не найдено фильмов по запросу {query}",
        )
    return persons


@router.get("/{person_id}/", response_model=Person)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    perm: bool = Depends(require_permissions([permissions.persons_can_view])),
) -> Person:
    """Получает информацию о персоне по ID"""

    person = await person_service.get_person_by_id(person_id=person_id)
    if person is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Не найдена персона с таким ID",
        )
    return person


@router.get("/{person_id}/films/", response_model=list[ShortFilm])
async def films_by_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
    perm: bool = Depends(require_permissions([permissions.persons_can_view])),
) -> list[ShortFilm]:
    """Получает фильмы персоны по его ID"""
    person = await person_service.get_person_by_id(person_id=person_id)
    if person is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Персона с ID {person_id} не найдена",
        )

    nested_filters = ["directors", "actors", "writers"]
    person_films = await film_service.get_person_films(
        person_id=person_id, nested_filters=nested_filters
    )
    if person_films is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Ошибка при получении фильмов",
        )
    return person_films
