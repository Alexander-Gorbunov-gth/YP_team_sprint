import uuid

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.services.users.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from src.services.users.interfacies import IUserService, UserRepository
from src.services.users.repositories import SqlmodelUserRepository
from src.services.users.schemas import UserCreate, UserResponse, UserUpdate
from ...db.postgres import get_session


class UserService(IUserService):

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(
        self, current_user: User, user_data: UserCreate
    ) -> UserResponse:
        try:
            return await self.user_repository.create(user_data)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    async def get_user(self, current_user: User, user_id: uuid.UUID):
        try:
            return await self.user_repository.get_by_id(user_id)
        except EntityNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    async def get_all_user(
        self, current_user: User, skip: 0, limit: 50
    ) -> list[UserResponse]:
        users = await self.user_repository.get_multi(skip, limit)
        return users

    async def update_user(
        self, current_user: User, user: User, user_data: UserUpdate
    ) -> UserResponse | None:
        try:
            return await self.user_repository.update(instance=user, schema=user_data)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    async def add_role_to_users(self, user, role):
        try:
            return await self.user_repository.add_role(instance=user, role=role)
        except EntityAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )


async def get_user_service(
    session: AsyncSession = Depends(get_session),
):
    user_repository: UserRepository = SqlmodelUserRepository(
        session=session, model=User
    )
    return UserService(user_repository=user_repository)
