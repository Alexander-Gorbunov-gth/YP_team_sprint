from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    async def add(self, item: T) -> T: ...

    @abstractmethod
    async def get_by_id(self, item_id: str) -> T | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[T]: ...

    @abstractmethod
    async def get_by_user_and_movie_uid(self, user_uid: UUID, movie_uid: UUID) -> T | None: ...

    @abstractmethod
    async def update(self, item: T) -> T | None: ...

    @abstractmethod
    async def delete(self, item_id: str) -> T | None: ...


class BeanieBaseRepository(AbstractRepository[T], ABC):

    def __init__(self, model: Document, domain_model: BaseModel):
        self._domain_model = domain_model
        self._model: Document = model

    async def add(self, item: T) -> T:
        """
        Добавляет документ в базу данных
        :param item: Документ для добавления
        :return: Добавленный документ
        """

        document = self._model(**item.model_dump())
        await document.insert()
        document.id = str(document.id)
        return self._domain_model.model_validate(document)

    async def get_by_id(self, item_id: str):
        """
        Получает документ из базы данных по ID
        :param item_id: ID документа
        :return: Документ
        """
        document = await self._model.get(item_id)
        if document is None:
            return None
        document.id = str(document.id)
        return self._domain_model.model_validate(document)

    async def get_by_user_id(self, user_uid: UUID, limit: int = 10, offset: int = 0) -> list[T]:
        """
        Получает документы из базы данных по ID пользователя
        :param user_uid: ID пользователя
        :param limit: Количество документов
        :param offset: Сдвиг
        :return: Список документов
        """

        documents = await self._model.find(self._model.user_uid == user_uid).skip(offset).limit(limit).to_list()
        for document in documents:
            document.id = str(document.id)
        return [self._domain_model.model_validate(document) for document in documents]

    async def get_by_user_and_movie_uid(self, user_uid: UUID, movie_uid: UUID) -> T | None:
        """
        Получает документ из базы данных по ID пользователя и ID фильма
        :param user_uid: ID пользователя
        :param movie_uid: ID фильма
        :return: Документ
        """

        document = await self._model.find_one(self._model.user_uid == user_uid, self._model.movie_uid == movie_uid)
        if document is None:
            return None
        document.id = str(document.id)
        return self._domain_model.model_validate(document)

    async def update(self, item: T) -> T | None:
        """
        Обновляет документ в базе данных
        :param T: Документ для обновления
        :return: Обновленный документ
        """

        document = await self._model.get(item.id)
        if document is None:
            return None
        for key, value in item.model_dump().items():
            setattr(document, key, value)
        await document.save()
        document.id = str(document.id)
        return self._domain_model.model_validate(document)

    async def delete(self, item_id: str) -> T | None:
        """
        Удаляет документ из базы данных
        :param item_id: ID документа для удаления
        :return: Удаленный документ
        """

        document = await self._model.get(item_id)
        if document is None:
            return None
        await document.delete()
        document.id = str(document.id)
        return self._domain_model.model_validate(document)
