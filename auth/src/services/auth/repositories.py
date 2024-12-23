from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Result, insert, update, select, delete

from src.services.auth.interfaces import ISQLAlchemyRepository
from src.models.interfaces import IModel

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class SQLAlchemyAuthRepository(ISQLAlchemyRepository):
    """Репозиторий для работы с базой данных с использованием SQLAlchemy."""

    async def add(self, schema: CreateSchema) -> IModel:
        """
        Добавляет новую запись в базу данных.

        :schema: данные для создания записи (Pydantic-схема).
        :return: созданный объект модели.
        """

        result: Result = await self._session.execute(
            insert(self._model).values(schema.model_dump()).returning(self._model)
        )
        return result.scalar_one()

    async def update(
        self, object_id: str | UUID, schema: UpdateSchema
    ) -> IModel | None:
        """
        Обновляет запись в базе данных по ее идентификатору.

        :object_id: идентификатор записи.
        :schema: данные для обновления записи (Pydantic-схема).
        :return: обновленный объект модели или None, если запись не найдена.
        """

        result: Result = await self._session.execute(
            update(self._model)
            .filter_by(id=object_id)
            .values(**schema.model_dump())
            .returning(self._model)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, object_id: str | UUID) -> IModel | None:
        """
        Получает запись из базы данных по ее идентификатору.

        :object_id: идентификатор записи.
        :return: объект модели или None, если запись не найдена.
        """

        result: Result = await self._session.execute(
            select(self._model).filter_by(id=object_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self, offset: int | None = None, limit: int | None = None
    ) -> list[IModel]:
        """
        Возвращает список записей из базы данных с учетом пагинации.

        :offset: количество записей, которые нужно пропустить (смещение).
        :limit: максимальное количество записей для возврата.
        :return: список объектов модели.
        """

        result: Result = await self._session.execute(
            select(self._model).offset(offset=offset).limit(limit=limit)
        )
        return result.scalars().all()

    async def delete(self, object_id: str | UUID) -> None:
        """
        Удаляет запись из базы данных по ее идентификатору.

        :object_id: идентификатор записи.
        """

        await self._session.execute(delete(self._model).filter_by(id=object_id))

    async def get_by_filters(self, **filters) -> list[IModel]:
        """
        Возвращает записи из базы данных, соответствующие указанным фильтрам.

        :kwargs: параметры фильтрации в формате ключ-значение (например, {"user_id": user_id}).
        :return: список объектов модели, соответствующих условиям фильтрации.
        """

        result: Result = await self._session.execute(
            select(self._model).filter_by(**filters)
        )
        return result.scalar_one_or_none()

    async def get_with_joins(self, *joined_settings, **filters) -> list[IModel]:
        """
        Универсальный метод для выполнения запроса с JOIN.

        :joined_settings: список кортежей (модель, условие JOIN).
        :filters: любые дополнительные фильтры, которые могут быть переданы.
        :return: список объектов модели, соответствующих условию.
        """
        query = select(self._model).select_from(self._model)

        for join_model, join_condition in joined_settings:
            query = query.join(join_model, join_condition)

        for field, value in filters.items():
            query = query.filter(getattr(self._model, field) == value)

        result: Result = await self._session.execute(query)
        return result.scalars().all()
