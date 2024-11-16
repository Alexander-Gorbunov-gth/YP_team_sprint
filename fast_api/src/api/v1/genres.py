from http import HTTPStatus
from typing import List, Optional
import logging

from fastapi import APIRouter, Depends,  HTTPException, Query
from pydantic import BaseModel
from fastapi_cache.decorator import cache

from src.models.film import Genre
from src.services.genres import GenreService, get_genre_service


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()


# поиск по жанрам с возможностью передачи query параметров 
@router.get('/search', response_model=List[Genre])
@cache(expire=60)
async def all_genres(genre_service: GenreService = Depends(get_genre_service),
                    query: Optional[str] = Query(None, alias="query"),
                    order: str = Query("asc", enum=["asc", "desc"]),
                    page_size: int = Query(10, gt=0, le=100),
                    page_number: int = Query(1, ge=1)
                    )->Optional[List[Genre]]:
    try:
        genres = await genre_service.get_all_genres(query, order, page_size, page_number)
        if not genres:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Жанры не найдены")
        return genres
    except Exception as e:
        logger.error(f"Ошибка при получении жанров: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Ошибка при получении жанров: {str(e)}")
    
    
# поиск по жанрам по id
@router.get('/{genre_id}', response_model=Genre)
@cache(expire=60)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    try:
        genre = await genre_service.get_by_id(genre_id)
        if not genre:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Жанр не найден')

        return Genre(id=genre.id, name=genre.name)
    
    except Exception as e:
        logger.error(f"Ошибка при поиске жанра по ID {genre_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Ошибка при получении жанра: {str(e)}")


