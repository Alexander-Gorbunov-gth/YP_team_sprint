import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from src.api.v1.depends import User, bookmark_serviceDep, get_current_user
from src.api.v1.schemas import BookmarkResponse, CreateBookmarkRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])


@router.post("/", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED, summary="Создание закладки")
async def create_bookmark(
    bookmark: CreateBookmarkRequest,
    service: bookmark_serviceDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> BookmarkResponse:
    """Создание закладки для фильма"""

    bookmark_response = await service.create_bookmark(current_user.sub, bookmark.movie_uid)
    return bookmark_response


@router.get(
    "/",
    response_model=list[BookmarkResponse],
    summary="Получение закладок пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_bookmarks_by_user_id(
    bookmark_service: bookmark_serviceDep,
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[BookmarkResponse]:
    """Получение закладок пользователя"""

    bookmarks = await bookmark_service.get_bookmarks_by_user_id(user_uid=current_user.sub, limit=limit, offset=offset)
    return bookmarks


@router.get(
    "/{bookmark_id}",
    response_model=BookmarkResponse,
    summary="Получение закладки по ID",
    status_code=status.HTTP_200_OK,
)
async def get_bookmark_by_id(
    bookmark_service: bookmark_serviceDep,
    current_user: Annotated[User, Depends(get_current_user)],
    bookmark_id: str = Path(..., description="ID закладки"),
) -> BookmarkResponse:
    """Получение закладки по ID"""

    bookmark = await bookmark_service.get_bookmark_by_id(bookmark_id=bookmark_id, user_uid=current_user.sub)
    return bookmark


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление закладки по ID")
async def delete_bookmark(
    bookmark_service: bookmark_serviceDep,
    current_user: Annotated[User, Depends(get_current_user)],
    bookmark_id: str = Path(..., description="ID закладки"),
) -> None:
    """Удаление закладки по ID"""

    await bookmark_service.delete_bookmark(bookmark_id=bookmark_id, user_uid=current_user.sub)
    return
