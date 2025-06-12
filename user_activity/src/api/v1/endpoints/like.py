from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from src.api.v1.depends import User, get_test_current_user, like_serviceDep
from src.api.v1.schemas import CreateLikeRequest, LikeCountResponse, LikeResponse

router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", response_model=LikeResponse, status_code=status.HTTP_201_CREATED, summary="Создать лайк")
async def create_like(
    like: CreateLikeRequest, service: like_serviceDep, current_user: Annotated[User, Depends(get_test_current_user)]
) -> LikeResponse:
    """Создать лайк."""

    like_response = await service.create_like(current_user.sub, like.movie_uid)
    return like_response


@router.get(
    "/", response_model=list[LikeResponse], summary="Получить лайки пользователя", status_code=status.HTTP_200_OK
)
async def get_likes_by_user_id(
    like_service: like_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[LikeResponse]:
    """Получить лайки пользователя."""

    likes = await like_service.get_likes_by_user_id(user_uid=current_user.sub, limit=limit, offset=offset)
    return likes


@router.get(
    "/{like_id}",
    response_model=LikeResponse,
    summary="Получить лайк по ID",
    status_code=status.HTTP_200_OK,
)
async def get_like_by_id(
    like_service: like_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
    like_id: str = Path(..., description="ID лайка"),
) -> LikeResponse:
    """Получить лайк по ID."""

    like = await like_service.get_like_by_id(like_id=like_id, user_uid=current_user.sub)
    return like


@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить лайк по ID")
async def delete_like(
    like_service: like_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
    like_id: str = Path(..., description="ID лайка"),
) -> None:
    """Удалить лайк по ID."""

    await like_service.delete_like(like_id=like_id, user_uid=current_user.sub)
    return


@router.get(
    "/movies/{movie_uid}",
    response_model=LikeCountResponse,
    summary="Получить лайки по ID фильма",
    status_code=status.HTTP_200_OK,
)
async def get_likes_count_by_movie_id(
    like_service: like_serviceDep,
    movie_uid: UUID = Path(..., description="ID фильма"),
) -> LikeCountResponse:
    """Получить лайки по ID фильма."""

    likes_count = await like_service.get_likes_count_by_movie_id(movie_uid=movie_uid)
    return LikeCountResponse(count=likes_count, movie_uid=movie_uid)
