import uuid

from fastapi import HTTPException, status

from src.models.users import User
from src.services.users.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    PermissionAssociationError,
)
from src.services.users.interfacies import IUserService, UserRepository
from src.services.users.schemas import UserCreate, UserResponse, UserUpdate


class UserService(IUserService):

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(
        self, current_user: User, user_data: UserCreate
    ) -> UserResponse:
        try:
            return await self.repository.create(user_data)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    async def get_user(self, current_user: User, user_id: uuid.UUID):
        try:
            return await self.repository.get_by_id(user_id)
        except EntityNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    async def get_all_user(
        self, current_user: User, skip: 0, limit: 50
    ) -> list[UserResponse]:
        users = await self.repository.get_multi(skip, limit)
        return users

    async def update_user(
        self, current_user: User, user: User, user_data: UserUpdate
    ) -> UserResponse | None:
        try:
            return await self.repository.update(instance=user, schema=user_data)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    async def assign_permission_to_user(self, user: User, permission_slug: str) -> None:
        try:
            return await self.repository.add_permission(user, permission_slug)
        except EntityNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    async def remove_permission_from_user(
        self, user: User, permission_slug: str
    ) -> None:
        try:
            await self.repository.remove_permission(user, permission_slug)
        except PermissionAssociationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )
