import logging

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.domain.entities import Permission, Role
from src.domain.exceptions import RoleIsExists
from src.domain.repositories import AbstractRoleRepository

logger = logging.getLogger(__name__)


class SQLAlchemyRoleRepository(AbstractRoleRepository):
    """Репозиторий для управления ролями в базе данных"""

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create_role(self, slug: str, title: str, permissions: list[Permission], description: str | None) -> Role:
        """Создаёт новую роль с заданными разрешениями"""
        insert_data = {"slug": slug, "title": title, "description": description}
        query = insert(Role).values(insert_data).returning(Role)
        try:
            result: Result = await self._session.execute(query)
            role = result.scalar_one()

            # Добавляем разрешения к роли
            for permission in permissions:
                await self._session.execute(
                    insert(Role.permissions).values(role_slug=role.slug, permission_slug=permission.slug)
                )

            await self._commit()
        except IntegrityError:
            logger.error("Роль с slug %s уже существует.", slug)
            raise RoleIsExists
        return role

    async def delete_role(self, role: Role) -> bool:
        """Удаляет роль"""
        query = delete(Role).filter_by(slug=role.slug)
        await self._session.execute(query)
        await self._commit()
        return True

    async def update_role(self, role: Role) -> Role | None:
        """Обновляет данные роли"""
        result: Result = await self._session.execute(
            update(Role)
            .filter_by(slug=role.slug)
            .values(title=role.title, description=role.description)
            .returning(Role)
        )
        await self._commit()
        return result.scalar_one_or_none()

    async def get_role(self, slug: str) -> Role | None:
        """Получает роль по slug"""
        query = select(Role).filter_by(slug=slug)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_roles(self) -> list[Role]:
        """Получает список всех ролей"""
        query = select(Role)
        result: Result = await self._session.execute(query)
        return result.scalars().all()

    async def _commit(self) -> None:
        """Фиксирует изменения в БД"""
        await self._session.commit()


def get_role_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyRoleRepository:
    """Функция для получения экземпляра репозитория"""
    return SQLAlchemyRoleRepository(session=session)
