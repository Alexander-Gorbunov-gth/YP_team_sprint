from fastapi import APIRouter, Depends, Form

from src.services.auth.service import AuthService, get_auth_service
from src.services.users.schemas import UserCreate
from src.services.auth.interfaces import IAuthService


auth_router = APIRouter()


@auth_router.post("/register/")
async def register(
    user_data: UserCreate,
    auth_service: IAuthService = Depends(get_auth_service),
):
    user = await auth_service.register(user=user_data)
    return user


@auth_router.post("/login/")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    permissions = await auth_service.login(email=email, password=password)
    return permissions


@auth_router.post("/logout/")
async def logout():
    pass


@auth_router.post("/change-password/")
async def change_password():
    pass


@auth_router.post("/token/refresh/")
async def token_refresh():
    pass


@auth_router.post("/close-sessions/")
async def close_sessions():
    pass
