from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import Depends, HTTPException, status
from src.domain.like import Like
from src.infrastructure.repositories.like import AbstractLikeRepository, get_like_repository


class AbstractLikeService(ABC):
    @abstractmethod
    async def create_like(self, user_uid: UUID, movie_uid: UUID) -> Like: ...

    @abstractmethod
    async def get_like_by_id(self, like_id: str, user_uid: UUID) -> Like: ...

    @abstractmethod
    async def get_likes_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Like]: ...

    @abstractmethod
    async def delete_like(self, like_id: str, user_uid: UUID) -> Like: ...

    @abstractmethod
    async def get_likes_count_by_movie_id(self, movie_uid: UUID) -> int: ...


class LikeService(AbstractLikeService):
    def __init__(self, repository: AbstractLikeRepository):
        self._repository = repository

    async def create_like(self, user_uid: UUID, movie_uid: UUID) -> Like:
        """Создать лайк
        :param user_uid: UUID пользователя
        :param movie_uid: UUID фильма
        :return: Созданный лайк.
        """

        like = await self._repository.get_by_user_and_movie_uid(user_uid=user_uid, movie_uid=movie_uid)

        if like:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Лайк уже существует")

        like = Like(user_uid=user_uid, movie_uid=movie_uid)
        like_response = await self._repository.add(item=like)
        return like_response

    async def get_like_by_id(self, like_id: str, user_uid: UUID) -> Like:
        """
        Получить лайк по ID
        :param like_id: ID лайка
        :param user_uid: UUID пользователя
        :return: лайк
        """

        like = await self._repository.get_by_id(like_id)

        if like is None:
            raise HTTPException(status_code=404, detail="Лайк не найден.")

        if like.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="Нет доступа.")

        return like

    async def get_likes_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Like]:
        """
        Получить лайки пользователя
        :param user_uid: UUID пользователя
        :param limit: Количество лайков
        :param offset: Сдвиг
        :return: Список лайков
        """

        return await self._repository.get_by_user_id(user_uid=user_uid, limit=limit, offset=offset)

    async def delete_like(self, like_id: str, user_uid: UUID) -> Like:
        """
        Удалить лайк
        :param like_id: ID лайка
        :param user_uid: UUID пользователя
        :return: Удаленный лайк
        """

        like = await self._repository.get_by_id(like_id)

        if like is None:
            raise HTTPException(status_code=404, detail="Лайк не найден.")

        if like.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="Нет доступа.")

        return await self._repository.delete(item_id=like_id)

    async def get_likes_count_by_movie_id(self, movie_uid: UUID) -> int:
        """
        Получить количество лайков по ID фильма
        :param movie_uid: ID фильма
        :return: Количество лайков
        """

        return await self._repository.get_likes_count_by_movie_id(movie_uid)


def get_like_service(repository: AbstractLikeRepository = Depends(get_like_repository)) -> AbstractLikeService:
    return LikeService(repository)
