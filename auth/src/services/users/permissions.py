from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.permissions import Permission
from src.models.roles import RolePermission
from src.models.users import User


def permission_required(required_permission: str):
    def permission_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            payload = kwargs.get("current_user")
            session: AsyncSession = kwargs.get("session")
            current_user = await session.get(User, payload.sub)

            if not current_user.role_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Недостаточно прав для действия: '{required_permission}'",
                )

            stmt = select(Permission).where(Permission.slug == required_permission)
            result = await session.execute(stmt)
            permission = result.scalar_one_or_none()

            if not permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Не иментся такие действия: '{required_permission}'",
                )

            stmt = select(RolePermission.permission_id).where(
                RolePermission.role_id == current_user.role_id
            )
            result = await session.execute(stmt)
            roles = result.scalars().all()

            if permission.id not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Не прав на такие действия: '{required_permission}'",
                )

            return await func(*args, **kwargs)

        return wrapper

    return permission_decorator
