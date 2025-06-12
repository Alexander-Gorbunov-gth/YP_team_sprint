from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import Depends, HTTPException
from pydantic import ValidationError
from src.domain.bookmark import Bookmark
from src.infrastructure.repositories.bookmark import AbstractBookmarkRepository, get_bookmark_repository


class AbstractBookmarkService(ABC):
    @abstractmethod
    async def create_bookmark(self, user_uid: UUID, movie_uid: UUID) -> Bookmark: ...

    @abstractmethod
    async def get_bookmark_by_id(self, bookmark_id: str, user_uid: UUID) -> Bookmark: ...

    @abstractmethod
    async def get_bookmarks_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Bookmark]: ...

    @abstractmethod
    async def delete_bookmark(self, bookmark_id: str, user_uid: UUID) -> Bookmark: ...


class BookmarkService(AbstractBookmarkService):
    def __init__(self, repository: AbstractBookmarkRepository):
        self._repository = repository

    async def create_bookmark(self, user_uid: UUID, movie_uid: UUID) -> Bookmark:
        """
        Создает закладку
        :param user_id: ID пользователя
        :param movie_id: ID фильма
        :return: Созданная закладка
        """

        try:
            bookmark = Bookmark(user_uid=user_uid, movie_uid=movie_uid)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

        if await self._repository.get_by_user_and_movie_uid(bookmark.user_uid, bookmark.movie_uid):
            raise HTTPException(status_code=400, detail="Закладка уже существует.")

        return await self._repository.add(bookmark)

    async def get_bookmark_by_id(self, bookmark_id: str, user_uid: UUID) -> Bookmark:
        """
        Получает закладку по ID
        :param bookmark_id: ID закладки
        :param user_id: ID пользователя
        :return: Закладка
        """

        try:
            bookmark = await self._repository.get_by_id(bookmark_id)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

        if bookmark is None:
            raise HTTPException(status_code=404, detail="Закладка не найдена.")

        if bookmark.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="У вас нет доступа к этой закладке.")

        return bookmark

    async def get_bookmarks_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[Bookmark]:
        """
        Получает закладки по ID пользователя
        :param user_id: ID пользователя
        :param limit: Количество закладок
        :param offset: Сдвиг
        :return: Список закладок
        """

        return await self._repository.get_by_user_id(user_uid=user_uid, limit=limit, offset=offset)

    async def delete_bookmark(self, bookmark_id: str, user_uid: UUID) -> Bookmark:
        """
        Удаляет закладку по ID
        :param bookmark_id: ID закладки
        :param user_id: ID пользователя
        :return: Удаленная закладка
        """

        bookmark = await self._repository.get_by_id(bookmark_id)
        if bookmark is None:
            raise HTTPException(status_code=404, detail="Закладка не найдена.")

        if bookmark.user_uid != user_uid:
            raise HTTPException(status_code=403, detail="У вас нет доступа к этой закладке.")

        return await self._repository.delete(bookmark_id)


def get_bookmark_service(
    repository: AbstractBookmarkRepository = Depends(get_bookmark_repository),
) -> AbstractBookmarkService:
    return BookmarkService(repository=repository)
