# from fastapi import APIRouter, Depends
# from typing import List

# from src.services.permissions import PermissionsService
# from src.schemas.permissions import PermissionPublic

# perm_router = APIRouter()


# @perm_router.get("/", response_model=list[PermissionPublic])
# async def get_all_permissions(
#     permissions: PermissionsService = Depends(PermissionsService().list)
# ):
#     return permissions


# @perm_router.get("/{slug}/", response_model=PermissionPublic)
# async def get_permission(
#     permission: PermissionsService = Depends(PermissionsService().get)
# ):
#     return permission


# @perm_router.post("/", response_model=PermissionPublic)
# async def create_permission(
#     permission: PermissionsService = Depends(PermissionsService().create)
# ):
#     return permission


# @perm_router.patch("/{slug}/", response_model=PermissionPublic)
# async def change_permissions(
#     permission: PermissionsService = Depends(PermissionsService().update)
# ):
#     return permission


# @perm_router.delete("/{slug}/")
# async def delete_permission(
#     permission: PermissionsService = Depends(PermissionsService().delete)
# ):
#     return permission
