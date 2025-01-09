from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.services.auth.helpers import extract_and_validate_token
from src.services.users.interfacies import IUserService, IRoleService
from src.services.users.role_services import get_role_service
from src.services.users.user_services import get_user_service


async def user_by_id(
    user_id: Annotated[UUID, Path],
    current_user=Depends(extract_and_validate_token),
    user_services: IUserService = Depends(get_user_service),
):
    return await user_services.get_user(current_user=current_user, user_id=user_id)


async def role_by_id(
    role_id: Annotated[UUID, Path],
    current_user=Depends(extract_and_validate_token),
    role_services: IRoleService = Depends(get_role_service),
):
    return await role_services.get_role_by_id(
        current_user=current_user, role_id=role_id
    )
