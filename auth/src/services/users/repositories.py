from typing import Generic, TypeVar, Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.permissions import Permission
from src.models.users import User
from src.services.users.exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
)
from .interfacies import UserRepository, IRoleRepository
from .schemas import RoleEnum
from ...models.roles import RolePermission

Model = TypeVar("Model")
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class SqlmodelUserRepository(
    UserRepository, Generic[Model, CreateSchema, UpdateSchema]
):
    def __init__(self, session: AsyncSession, model: Type[Model]):
        self._session = session
        self._model = model

    async def create(self, schema: CreateSchema) -> Model:
        try:
            instance = self._model(**schema.model_dump())
            self._session.add(instance)
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(
                f"{self._model.__name__} с такими данными уже существует"
            )

    async def update(self, instance: Model, schema: UpdateSchema) -> Model:
        try:
            for field, value in schema.model_dump(exclude_unset=True).items():
                setattr(instance, field, value)
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(
                f"Обновление {self._model.__name__} невозможно - конфликт с существующими данными"
            )

    async def delete(self, instance: Model) -> bool:
        await self._session.delete(instance)
        await self._session.commit()
        return True

    async def get_by_id(self, id: UUID) -> Model | None:
        instance = await self._session.get(self._model, id)
        if not instance:
            raise EntityNotFoundError(f"{self._model.__name__} с id={id} не найден")
        return instance

    async def get_multi(self, skip: int, limit: int) -> list[Model]:
        stmt = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_email(self, email: str) -> User | None:
        """
        Асинхронный метод для получения пользователя из базы данных по его email.

        Args:
            email (str): Электронная почта пользователя, по которой выполняется поиск.

        Returns:
            User | None: Экземпляр объекта User, если пользователь с указанным email найден.
                         Если пользователь не найден, возвращает None.
        """
        result: Result = await self._session.execute(
            select(User).filter_by(email=email)
        )
        return result.scalar_one_or_none()

    async def add_role(self, instance: Model, role):
        try:
            setattr(instance, "role_id", role.id)
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(
                f"{self._model.__name__} с такими данными уже существует"
            )


class RoleRepository(IRoleRepository):

    def __init__(self, session: AsyncSession, model: Model):
        self._session = session
        self._model = model

    async def create(self, role_title: RoleEnum) -> Model:
        try:
            instance = self._model(title=role_title)
            self._session.add(instance)
            await self._session.commit()
            return instance
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(
                f"{self._model.__name__} с такими названием уже существует"
            )

    async def get_by_id(self, role_id: UUID):
        instance = await self._session.get(self._model, role_id)
        if not instance:
            raise EntityNotFoundError(
                f"{self._model.__name__} с id={role_id} не найден"
            )
        return instance

    async def assign_permissions(self, role, permission_slug):
        stmt = select(Permission).where(Permission.slug == permission_slug)
        result = await self._session.execute(stmt)
        permission = result.scalar_one_or_none()
        if not permission:
            raise EntityNotFoundError(f"Объект с slug - {permission_slug} не найден")

        try:
            role_permission = RolePermission(
                role_id=role.id, permission_id=permission.id
            )
            self._session.add(role_permission)
            await self._session.commit()

            return role_permission
        except IntegrityError:
            await self._session.rollback()
            raise EntityAlreadyExistsError(
                f"{self._model.__name__} с такими данными уже существует"
            )
