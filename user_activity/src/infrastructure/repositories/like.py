from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.like import Like
from src.infrastructure.models import LikeModel
from src.infrastructure.repositories.base import AbstractRepository, BeanieBaseRepository


class AbstractLikeRepository(AbstractRepository[Like], ABC):
    @abstractmethod
    async def get_likes_count_by_movie_id(self, movie_uid: UUID) -> int: ...


class LikeRepository(AbstractLikeRepository, BeanieBaseRepository[Like]):
    """Репозиторий для работы с лайками"""

    async def get_likes_count_by_movie_id(self, movie_uid: UUID) -> int:
        """
        Получить количество лайков для фильма
        :param movie_uid: UUID фильма
        :return: количество лайков
        """

        likes_count = await self._model.find(self._model.movie_uid == movie_uid).count()
        return likes_count


def get_like_repository() -> AbstractLikeRepository:
    return LikeRepository(model=LikeModel, domain_model=Like)
