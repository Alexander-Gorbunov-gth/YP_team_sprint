from functools import lru_cache
import uuid
from datetime import datetime, timedelta

from fastapi import Depends

from sqlalchemy.exc import IntegrityError
from src.schemas.users import TokenUserData
from src.models.users import User
from src.models.permissions import Permission
from src.models.roles import Role, RolePermission
from src.services.auth.uow import get_auth_uow
from src.services.users.schemas import UserResponse, UserCreate
from src.services.auth.interfaces import IAuthService, IAuthUoW
from src.services.auth.exceptions import (
    UserIsExist,
    UserNotFoundError,
    InvalidPasswordError,
)
from src.services.auth.password import get_password_hash, verify_password
from src.core.config import settings

ACCESS_EXPIRE_MINUTES = settings.service.access_token_expire
REFRESH_EXPIRE_DAYS = settings.service.refresh_token_expire


class AuthService(IAuthService):
    def __init__(self, uow: IAuthUoW) -> None:
        self._uow: IAuthUoW = uow

    async def register(self, user: UserCreate) -> User:
        async with self._uow as uow:
            user.password = get_password_hash(user.password)
            try:
                user = await uow.users.add(user)
            except IntegrityError:
                raise UserIsExist
            return UserResponse(**await user.to_dict())

    async def login(self, email: str, password: str):
        async with self._uow as uow:
            user = await uow.users.get_by_filters(email=email)
            print(user)
            if user is None:
                raise UserNotFoundError
            if not verify_password(password=password, hashed_password=user.password):
                raise InvalidPasswordError
            role = user.role.permissions
            print(role)

            return user

    @staticmethod
    def _generated_user_data(
        user: User, permissions: list | None = None
    ) -> TokenUserData:
        user_data = TokenUserData(
            sub=user.id,
            scope=permissions if permissions is not None else [],
            iat=datetime.utcnow(),
            access_exp=datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES),
            refresh_exp=datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS),
            jti=uuid.uuid4(),
        )
        return user_data

    async def _get_user_by_email_and_validate_password():
        pass


# def password_hash(password: str) -> str:
#     hashable_password =
#     pass


@lru_cache
def get_auth_service(uow: IAuthUoW = Depends(get_auth_uow)) -> IAuthService:
    auth_service: IAuthService = AuthService(uow=uow)
    return auth_service
