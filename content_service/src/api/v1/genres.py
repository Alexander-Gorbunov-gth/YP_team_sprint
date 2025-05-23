import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from src.core.auth import require_permissions
from src.core.permissions import permissions
from src.models.genre import Genre
from src.services.genres import GenreService, get_genre_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    perm: bool = Depends(require_permissions([permissions.genres_can_view])),
) -> Genre:

    genre = await genre_service.get_by_id(genre_id=genre_id)
    if genre is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Жанр не с id {genre_id} не найден",
        )
    return genre


@router.get("/", response_model=list[Genre])
async def all_genres(
    genre_service: GenreService = Depends(get_genre_service),
    page_size: int = Query(10, gt=0, le=100),
    page: int = Query(1, ge=1),
    perm: bool = Depends(require_permissions([permissions.genres_can_view])),
) -> list[Genre] | None:
    genres = await genre_service.get_all_genres(
        sort=None, page_size=page_size, page=page
    )
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Жанры не найдены"
        )
    return genres
