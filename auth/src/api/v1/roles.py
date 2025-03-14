from fastapi import APIRouter, Depends

from src.api.v1.schemas.permissions import PermissionCreate, PermissionResponse
from src.services.role import RoleService, get_role_service

roles_router = APIRouter()


@roles_router.get("/", response_model=list[PermissionResponse])
async def get_all_roles(role_service: RoleService = Depends(get_role_service)):
    return await role_service.get()


@roles_router.get("/{slug}/", response_model=PermissionResponse)
async def get_role(slug: str, role_service: RoleService = Depends(get_role_service)):
    return await role_service.get(slug=slug)


@roles_router.post("/", response_model=PermissionResponse)
async def create_role(data: PermissionCreate, role_service: RoleService = Depends(get_role_service)):
    return await role_service.create_or_update(data=data)


@roles_router.patch("/{slug}/", response_model=PermissionResponse)
async def change_role(
    slug: str,
    data: PermissionCreate,
    role_service: RoleService = Depends(get_role_service),
):
    return await role_service.create_or_update(data=data, slug=slug)


@roles_router.delete("/{slug}/", response_model=bool)
async def delete_role(slug: str, role_service: RoleService = Depends(get_role_service)):
    return await role_service.delete(slug=slug)
