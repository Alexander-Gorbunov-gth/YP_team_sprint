import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
# from src.api.v1.schemas.events import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

@router.post("/event/{uuid}", summary="Оценить мероприятие")
async def evaluation():
    return

@router.post("/comments/{uuid}", summary="Добавить комментарии к мероприятию")
async def comment():
    return

@router.get("/event/{uuid}", summary="Получить оценку мероприятия")
async def get_evaluation():
    return

@router.get("/comments/{uuid}", summary="Получить комментарии к мероприятию")
async def get_comments():
    return

@router.get("/", summary="Получить рейтинг мероприятий")
async def get_raiting():
    return