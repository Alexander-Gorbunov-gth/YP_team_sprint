from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.review import Review
from src.infrastructure.models import ReviewModel
from src.infrastructure.repositories.base import AbstractRepository, BeanieBaseRepository


class AbstractReviewRepository(AbstractRepository[Review], ABC):

    @abstractmethod
    async def get_by_movie_id(self, movie_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_count_by_movie_id(self, movie_uid: UUID) -> int: ...

    @abstractmethod
    async def get_reviews_average_by_movie_id(self, movie_uid: UUID) -> float: ...


class ReviewRepository(AbstractReviewRepository, BeanieBaseRepository[Review]):
    """Репозиторий для работы с рецензиями"""

    async def get_by_movie_id(self, movie_uid: UUID, limit: int = 10, offset: int = 0) -> list[Review]:
        """
        Получение рецензий по ID фильма
        :param movie_uid: ID фильма
        :param limit: Количество рецензий
        :param offset: Сдвиг
        :return: Список рецензий
        """

        reviews = await self._model.find(self._model.movie_uid == movie_uid).skip(offset).limit(limit).to_list()
        for review in reviews:
            review.id = str(review.id)
        return [self._domain_model.model_validate(review) for review in reviews]

    async def get_reviews_count_by_movie_id(self, movie_uid: UUID) -> int:
        """
        Получение количества рецензий по ID фильма
        :param movie_uid: ID фильма
        :return: Количество рецензий
        """

        reviews_count = await self._model.find(self._model.movie_uid == movie_uid).count()
        return reviews_count

    async def get_reviews_average_by_movie_id(self, movie_uid: UUID) -> float:
        """
        Получение среднего рейтинга по ID фильма
        :param movie_uid: ID фильма
        :return: Средний рейтинг
        """

        reviews_average = await self._model.find(self._model.movie_uid == movie_uid).avg(self._model.rating)
        return reviews_average


def get_review_repository() -> AbstractReviewRepository:
    return ReviewRepository(model=ReviewModel, domain_model=Review)
