from fastapi import APIRouter, Depends, Query

from src.api.v1.dependencies import role_by_id
from src.services.users.interfacies import IRoleService
from src.services.users.role_services import get_role_service
from src.services.users.schemas import RoleEnum, UserRole

role_router = APIRouter()


@role_router.post("/create_role/", response_model=UserRole)
async def create_role(
    role_title: RoleEnum = Query(...),
    role_service: IRoleService = Depends(get_role_service),
):
    return await role_service.create_role(current_user=None, role_title=role_title)


@role_router.get("/{role_id}", response_model=UserRole)
async def get_role(role: UserRole = Depends(role_by_id)):
    return role


@role_router.post("/{role_id}/add-permissions")
async def add_role_permissions(
    permission_slug: str,
    role: UserRole = Depends(role_by_id),
    role_service: IRoleService = Depends(get_role_service),
):
    return await role_service.assign_permission(
        role=role, permission_slug=permission_slug
    )
