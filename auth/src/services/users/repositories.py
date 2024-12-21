from typing import Generic, TypeVar, Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.permissions import UserPermissionsAssociation, Permission
from src.services.users.exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    PermissionAssociationError,
)
from .interfacies import UserRepository

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

    async def add_permission(self, instance: Model, slug: str):
        permission = await self._session.get(Permission, slug)
        if not permission:
            raise EntityNotFoundError(f"Объект с slug - {slug} не найден")

        association = UserPermissionsAssociation(
            user_id=instance.id, permission_slug=permission
        )
        self._session.add(association)
        await self._session.commit()
        await self._session.refresh(association)
        return association

    async def remove_permission(self, instance: Model, slug: str):

        stmt = select(UserPermissionsAssociation).where(
            UserPermissionsAssociation.user_id == instance.id,
            UserPermissionsAssociation.permission_slug == slug,
        )
        result = await self._session.execute(stmt)
        association = result.scalar_one_or_none()

        if not association:
            raise PermissionAssociationError(
                f"Разрешение {slug} не привязано к пользователю {instance.login}"
            )

        await self._session.delete(association)
        await self._session.commit()
