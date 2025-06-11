from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import Depends, HTTPException
from src.domain.review import Review
from src.infrastructure.repositories.review import AbstractReviewRepository, get_review_repository


class AbstractReviewService(ABC):
    @abstractmethod
    async def create_review(self, user_uid: UUID, movie_uid: UUID, rating: int, content: str) -> Review: ...

    @abstractmethod
    async def get_review_by_id(self, review_id: UUID) -> Review: ...

    @abstractmethod
    async def get_reviews_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_by_movie_id(self, movie_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_count_by_movie_id(self, movie_uid: UUID) -> int: ...

    @abstractmethod
    async def get_reviews_average_by_movie_id(self, movie_uid: UUID) -> float: ...

    @abstractmethod
    async def update_review(self, review_id: UUID, user_uid: UUID, rating: int, content: str) -> Review: ...

    @abstractmethod
    async def delete_review(self, review_id: UUID) -> None: ...


class ReviewService(AbstractReviewService):
    """Сервис для работы с рецензиями"""

    def __init__(self, repository: AbstractReviewRepository):
        self._repository = repository

    async def create_review(self, user_uid: UUID, movie_uid: UUID, rating: int, content: str) -> Review:
        """
        Создание рецензии
        :param user_uid: ID пользователя
        :param movie_uid: ID фильма
        :param rating: Оценка
        :param content: Контент
        :return: Рецензия
        """

        review = Review.create(movie_uid=movie_uid, user_uid=user_uid, rating=rating, content=content)
        review_is_exists = await self._repository.get_by_user_and_movie_uid(user_uid=user_uid, movie_uid=movie_uid)
        if review_is_exists:
            raise HTTPException(status_code=400, detail="Оценка уже существует.")
        review_created = await self._repository.add(item=review)
        return review_created

    async def get_review_by_id(self, review_id: UUID) -> Review:
        """
        Получение рецензии по ID
        :param review_id: ID рецензии
        :return: Рецензия
        """

        review = await self._repository.get_by_id(item_id=review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Рецензия не найдена.")
        return review

    async def get_reviews_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]:
        """
        Получение рецензий по ID пользователя
        :param user_uid: ID пользователя
        :param limit: Количество рецензий
        :param offset: Сдвиг
        :return: Список рецензий
        """

        reviews = await self._repository.get_by_user_id(user_uid=user_uid, limit=limit, offset=offset)
        return reviews

    async def get_reviews_by_movie_id(self, movie_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]:
        """
        Получение рецензий по ID фильма
        :param movie_uid: ID фильма
        :param limit: Количество рецензий
        :param offset: Сдвиг
        :return: Список рецензий
        """

        reviews = await self._repository.get_by_movie_id(movie_uid=movie_uid, limit=limit, offset=offset)
        return reviews

    async def get_reviews_count_by_movie_id(self, movie_uid: UUID) -> int:
        """
        Получение количества рецензий по ID фильма
        :param movie_uid: ID фильма
        :return: Количество рецензий
        """
        return await self._repository.get_reviews_count_by_movie_id(movie_uid=movie_uid)

    async def get_reviews_average_by_movie_id(self, movie_uid: UUID) -> float:
        """
        Получение среднего рейтинга по ID фильма
        :param movie_uid: ID фильма
        :return: Средний рейтинг
        """
        reviews_average = await self._repository.get_reviews_average_by_movie_id(movie_uid=movie_uid)
        return round(reviews_average, 1)

    async def update_review(self, review_id: UUID, user_uid: UUID, rating: int, content: str) -> Review:
        """
        Обновление рецензии
        :param review_id: ID рецензии
        :param rating: Оценка
        :param content: Контент
        :return: Рецензия
        """

        review = await self._repository.get_by_id(item_id=review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Рецензия не найдена.")

        if review.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="У вас нет доступа к этой рецензии.")

        review.rating = rating
        review.content = content
        return await self._repository.update(item=review)

    async def delete_review(self, review_id: UUID, user_uid: UUID) -> None:
        """
        Удаление рецензии
        :param review_id: ID рецензии
        :return: None
        """

        review = await self._repository.get_by_id(item_id=review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Рецензия не найдена.")

        if review.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="У вас нет доступа к этой рецензии.")

        await self._repository.delete(item_id=review_id)
        return None


def get_review_service(repository: AbstractReviewRepository = Depends(get_review_repository)) -> AbstractReviewService:
    return ReviewService(repository=repository)
