from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from src.api.v1.depends import User, get_test_current_user, review_serviceDep
from src.api.v1.schemas import (
    CreateReviewRequest,
    ReviewAverageResponse,
    ReviewCountResponse,
    ReviewResponse,
    UpdateReviewRequest,
)

router = APIRouter(prefix="/review", tags=["Review"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED, summary="Создать рецензию")
async def create_review(
    review: CreateReviewRequest,
    review_service: review_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
) -> ReviewResponse:
    """Создать рецензию."""

    review_response = await review_service.create_review(
        current_user.sub, review.movie_uid, review.rating, review.content
    )
    return review_response


@router.get(
    "/movies/{movie_uid}",
    response_model=list[ReviewResponse],
    summary="Получить рецензии по ID фильма",
    status_code=status.HTTP_200_OK,
)
async def get_reviews_by_movie_id(
    review_service: review_serviceDep,
    movie_uid: UUID = Path(..., description="ID фильма"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ReviewResponse]:
    """Получить рецензии по ID фильма."""

    reviews = await review_service.get_reviews_by_movie_id(movie_uid=movie_uid, limit=limit, offset=offset)
    return reviews


@router.get(
    "/users/{user_uid}",
    response_model=list[ReviewResponse],
    summary="Получить рецензии по ID пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_reviews_by_user_id(
    review_service: review_serviceDep,
    user_uid: UUID = Path(..., description="ID пользователя"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ReviewResponse]:
    """Получить рецензии по ID пользователя."""

    reviews = await review_service.get_reviews_by_user_id(user_uid=user_uid, limit=limit, offset=offset)
    return reviews


@router.get(
    "/{review_id}", response_model=ReviewResponse, summary="Получить рецензию по ID", status_code=status.HTTP_200_OK
)
async def get_review_by_id(
    review_service: review_serviceDep,
    review_id: str = Path(..., description="ID рецензии"),
) -> ReviewResponse:
    """Получить рецензию по ID."""

    review = await review_service.get_review_by_id(review_id=review_id)
    return review


@router.patch(
    "/{review_id}", response_model=ReviewResponse, summary="Обновить рецензию", status_code=status.HTTP_200_OK
)
async def update_review(
    review: UpdateReviewRequest,
    review_service: review_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
    review_id: str = Path(..., description="ID рецензии"),
) -> ReviewResponse:
    """Обновить рецензию."""

    review_response = await review_service.update_review(
        review_id=review_id, user_uid=current_user.sub, rating=review.rating, content=review.content
    )
    return review_response


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить рецензию по ID")
async def delete_review(
    review_service: review_serviceDep,
    current_user: Annotated[User, Depends(get_test_current_user)],
    review_id: str = Path(..., description="ID рецензии"),
) -> None:
    """Удалить рецензию."""

    await review_service.delete_review(review_id=review_id, user_uid=current_user.sub)
    return


@router.get(
    "/movies/{movie_uid}/count",
    response_model=ReviewCountResponse,
    summary="Получить количество рецензий по ID фильма",
    status_code=status.HTTP_200_OK,
)
async def get_reviews_count_by_movie_id(
    review_service: review_serviceDep,
    movie_uid: UUID = Path(..., description="ID фильма"),
) -> ReviewCountResponse:
    """Получить количество рецензий по ID фильма."""

    reviews_count = await review_service.get_reviews_count_by_movie_id(movie_uid=movie_uid)
    return ReviewCountResponse(count=reviews_count, movie_uid=movie_uid)


@router.get(
    "/movies/{movie_uid}/average",
    response_model=ReviewAverageResponse,
    summary="Получить средний рейтинг по ID фильма",
    status_code=status.HTTP_200_OK,
)
async def get_reviews_average_by_movie_id(
    review_service: review_serviceDep,
    movie_uid: UUID = Path(..., description="ID фильма"),
) -> ReviewAverageResponse:
    """Получить средний рейтинг по ID фильма."""

    reviews_average = await review_service.get_reviews_average_by_movie_id(movie_uid=movie_uid)
    return ReviewAverageResponse(average=reviews_average, movie_uid=movie_uid)
