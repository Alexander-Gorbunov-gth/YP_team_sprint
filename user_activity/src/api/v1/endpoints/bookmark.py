import uuid

from fastapi import APIRouter, Path, status
from src.api.v1.depends import bookmark_serviceDep
from src.api.v1.schemas import CreateBookmarkRequest, CreateBookmarkResponse

router = APIRouter(prefix="/bookmark", tags=["Bookmark"])


@router.post(
    "/", response_model=CreateBookmarkResponse, status_code=status.HTTP_201_CREATED, summary="Создание закладки"
)
async def create_bookmark(bookmark: CreateBookmarkRequest, service: bookmark_serviceDep) -> CreateBookmarkResponse:
    """Создание закладки для фильма"""

    user_uid = uuid.uuid4()
    bookmark_response = await service.create_bookmark(user_uid, bookmark.movie_uid)
    return bookmark_response


@router.get(
    "/{user_uid}/bookmarks",
    response_model=list[CreateBookmarkResponse],
    summary="Получение закладок пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_bookmarks_by_user_id(
    bookmark_service: bookmark_serviceDep,
    user_uid: uuid.UUID = Path(..., description="UUID пользователя"),
) -> list[CreateBookmarkResponse]:
    """Получение закладок пользователя"""

    bookmarks = await bookmark_service.get_bookmarks_by_user_id(user_uid)
    return bookmarks


@router.get(
    "/{bookmark_id}",
    response_model=CreateBookmarkResponse,
    summary="Получение закладки по ID",
    status_code=status.HTTP_200_OK,
)
async def get_bookmark_by_id(
    bookmark_service: bookmark_serviceDep, bookmark_id: str = Path(..., description="ID закладки")
) -> CreateBookmarkResponse:
    """Получение закладки по ID"""

    bookmark = await bookmark_service.get_bookmark_by_id(bookmark_id)
    return bookmark


@router.delete("/{bookmark_id}")
async def delete_bookmark():
    pass
