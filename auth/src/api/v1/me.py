from fastapi import APIRouter, Depends

from src.services.auth.helpers import extract_and_validate_token
from src.services.users.interfacies import IUserService
from src.services.users.schemas import UserProfile
from src.services.users.user_services import get_user_service

me_router = APIRouter()


@me_router.get("/", response_model=UserProfile)
async def my_profile(
    current_user=Depends(extract_and_validate_token),
    user_services: IUserService = Depends(get_user_service),
):
    user_id = current_user.sub
    return await user_services.get_user(current_user=current_user, user_id=user_id)


@me_router.get("/{uuid}/sessions/")
async def my_sessions():
    pass
