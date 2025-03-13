from fastapi import APIRouter, Depends
from typing import List

from src.services.permission import get_permission_service, PermissionService
from src.api.v1.schemas.permissions import (
    PermissionResponse,
    PermissionCreate
)

roles_rouner = APIRouter()


@roles_rouner.get("/", response_model=list[PermissionResponse])
async def get_all_roles(
    permisson_service: PermissionService = Depends(get_permission_service)
):
    return permisson_service.get()


@roles_rouner.get("/{slug}/", response_model=[PermissionResponse])
async def get_role(
    slug: str,
    permisson_service: PermissionService = Depends(get_permission_service)
):
    return permisson_service.get(slug=slug)


@roles_rouner.post("/", response_model=PermissionResponse)
async def create_role(
    data: PermissionCreate,
    permisson_service: PermissionService = Depends(get_permission_service)
):
    return permisson_service.create_or_update(data=data)


@roles_rouner.patch("/{slug}/", response_model=PermissionResponse)
async def change_role(
    slug: str,
    data: PermissionCreate,
    permisson_service: PermissionService = Depends(get_permission_service)
):
    return permisson_service.create_or_update(data=data, slug=slug)


@roles_rouner.delete("/{slug}/", response_model=bool)
async def delete_role(
    slug: str,
    permisson_service: PermissionService = Depends(get_permission_service)
):
    return permisson_service.delete(slug=slug)
