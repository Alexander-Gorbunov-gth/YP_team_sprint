import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from pydantic import BaseModel


from src.db.postgres import get_session
from src.models.permissions import PermissionCreate, Permission, PermissionPublic, PermissionUpdate

logger = logging.getLogger(__name__)


class PermissionsService:

    def __init__(self) -> None:
        pass

    async def create(
        self,
        data: PermissionCreate,
        db: AsyncSession = Depends(get_session)
    ):
        obj_in_db = await db.scalar(exists().where(Permission.slug == data.slug).select())
        if obj_in_db:
            raise HTTPException(status_code=409, detail=f"Объект с slug - {data.slug} уже существует")
        permission = Permission(**data.model_dump())
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission

    async def get(
        self,
        slug: str,
        db: AsyncSession = Depends(get_session)
    ):
        permission = await db.get(Permission, slug)
        if not permission:
            raise HTTPException(status_code=404, detail=f"Объект с slug - {slug} не найден")
        return permission
    
    async def list(
        self,
        db: AsyncSession = Depends(get_session)
    ):
        permissions = await db.scalars(
            select(Permission)
        )
        permission_list = permissions.all()
        return permission_list

    async def update(
        self,
        slug: str,
        data: PermissionUpdate,
        db: AsyncSession = Depends(get_session)  
    ):
        permission = await db.get(Permission, slug)
        if not permission:
            raise HTTPException(status_code=404, detail=f"Объект с slug - {slug} не найден")
        for k, v in data.model_dump().items():
            if v:
                setattr(permission, k, v)
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission

    async def delete(
        self,
        slug: str,
        db: AsyncSession = Depends(get_session)
    ):
        permission = await db.get(Permission, slug)
        if not permission:
            raise HTTPException(status_code=404, detail=f"Объект с slug - {slug} не найден")
        await db.delete(permission)
        await db.commit()
        return {"detail": f"Permission {slug} удален"}
