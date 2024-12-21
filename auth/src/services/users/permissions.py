from fastapi import HTTPException, status

from src.models.users import User


def permission_required(required_permission: str):
    def permission_decorator(func):
        async def wrapper(*args, **kwargs):
            current_user: User = kwargs.get("current_user")

            if current_user.is_superuser:
                return await func(*args, **kwargs)

            has_permission = any(
                permission.slug == required_permission
                for permission in current_user.permissions
            )
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Недостаточно прав для действия: '{required_permission}'",
                )

            return await func(*args, **kwargs)
        return wrapper
    return permission_decorator
