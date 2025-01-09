from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.models.users import User
from src.services.auth.helpers import extract_and_validate_token
from src.services.users import schemas
from src.services.users.interfacies import IUserService
from src.services.users.permissions import permission_required
from src.services.users.schemas import UserRole
from src.services.users.user_services import get_user_service
from .dependencies import user_by_id, role_by_id

users_router = APIRouter()


@users_router.post("/", response_model=schemas.UserResponse)
async def create_user(
    user: schemas.UserCreate,
    current_user=Depends(extract_and_validate_token),
    user_service: IUserService = Depends(get_user_service),
):
    return await user_service.create_user(current_user=current_user, user_data=user)


@users_router.get("/{user_id}/", response_model=schemas.UserResponse)
async def get_user(user: User = Depends(user_by_id)):
    return user


@users_router.get("/", response_model=list[schemas.UserResponse])
@permission_required("edit.users")
async def get_all_users(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(extract_and_validate_token),
    user_service: IUserService = Depends(get_user_service),
    skip: int = 0,
    limit: int = 50,
):
    return await user_service.get_all_user(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@users_router.patch("/{user_id}/", response_model=schemas.UserResponse)
async def change_user(
    user_in: schemas.UserUpdate,
    user: User = Depends(user_by_id),
    user_service: IUserService = Depends(get_user_service),
):
    return await user_service.update_user(
        current_user=None, user=user, user_data=user_in
    )


@users_router.post("/{user_id}/add-role/")
async def add_role_users(
    user: User = Depends(user_by_id),
    role: UserRole = Depends(role_by_id),
    user_services: IUserService = Depends(get_user_service),
):
    return await user_services.add_role_to_users(user, role)
