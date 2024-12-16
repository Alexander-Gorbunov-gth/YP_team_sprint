from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.models.users import User
from src.users import schemas
from src.users.injective import Container
from src.users.interfacies import IUserService
from .dependencies import user_by_id

users_router = APIRouter()


@users_router.get("/", response_model=list[schemas.UserResponse])
@inject
async def get_all_users(
    # current_user=Depends(get_current_user),
    user_service: IUserService = Depends(Provide[Container.user_service]),
    skip: int = 0,
    limit: int = 50,
):
    return await user_service.get_all_user(
        current_user=None,
        skip=skip,
        limit=limit,
    )


@users_router.post("/", response_model=schemas.UserResponse)
@inject
async def create_user(
    # current_user = Depends(get_current_user),
    user: schemas.UserCreate,
    user_service: IUserService = Depends(Provide[Container.user_service]),
):
    return await user_service.create_user(current_user=None, user_data=user)


@users_router.get("/{user_id}/", response_model=schemas.UserResponse)
async def get_user(user: User = Depends(user_by_id)):
    return user


@users_router.patch("/{user_id}/", response_model=schemas.UserResponse)
@inject
async def change_user(
    user_in: schemas.UserUpdate,
    user: User = Depends(user_by_id),
    user_service: IUserService = Depends(Provide[Container.user_service]),
):
    return await user_service.update_user(
        current_user=None, user=user, user_data=user_in
    )


@users_router.patch("/{user_id}/add-permissions/")
@inject
async def add_permission(
    permission_slug: str,
    user: User = Depends(user_by_id),
    user_services: IUserService = Depends(Provide[Container.user_service]),
):
    return await user_services.assign_permission_to_user(user, permission_slug)


@users_router.delete("/{user_id}/remove-permissions/")
@inject
async def remove_permission(
    permission_slug: str,
    user: User = Depends(user_by_id),
    user_services: IUserService = Depends(Provide[Container.user_service]),
):
    return await user_services.remove_permission_from_user(user, permission_slug)
