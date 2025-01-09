import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.roles import Role
from src.models.users import User
from src.services.users.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from src.services.users.interfacies import IRoleService, IRoleRepository
from src.services.users.repositories import RoleRepository
from src.services.users.schemas import RoleEnum


class RoleService(IRoleService):

    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    async def create_role(self, current_user: User, role_title: RoleEnum):
        try:
            return await self.role_repository.create(role_title=role_title)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    async def get_role_by_id(self, current_user: User, role_id: uuid.UUID):
        try:
            return await self.role_repository.get_by_id(role_id)
        except EntityNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    async def assign_permission(self, role, permission_slug):
        try:
            return await self.role_repository.assign_permissions(role, permission_slug)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )
        except EntityNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


async def get_role_service(
    session: AsyncSession = Depends(get_session),
):
    role_repository: IRoleRepository = RoleRepository(session=session, model=Role)
    return RoleService(role_repository=role_repository)
