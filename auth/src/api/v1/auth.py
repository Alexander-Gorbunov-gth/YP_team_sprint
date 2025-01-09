from fastapi import APIRouter, Depends, Form, Request, status

from src.schemas.users import TokenResponse, Payload
from src.services.auth.helpers import extract_and_validate_token
from src.services.auth.interfaces import IAuthService
from src.services.auth.service import AuthService, get_auth_service
from src.services.users.schemas import UserCreate

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
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    headers = request.headers
    refresh_token, access_token = await auth_service.login(
        email=email, password=password, headers=headers
    )
    return access_token


@auth_router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: Payload = Depends(extract_and_validate_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    await auth_service.logout(jti=payload.jti)
    return


@auth_router.post("/change-password/")
async def change_password():
    pass


@auth_router.post("/token/refresh/")
async def token_refresh():
    pass


@auth_router.post("/close-sessions/")
async def close_sessions():
    pass
