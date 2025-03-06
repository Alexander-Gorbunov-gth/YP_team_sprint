from fastapi import APIRouter, Depends, Request, status

from src.domain.entities import Token
from src.domain.exceptions import PasswordsNotMatch
from src.domain.interfaces import AbstractJWTService, AbstractAuthService
from src.services.auth import get_auth_service
from src.services.jwt import get_jwt_service
from src.api.v1.schemas.auth_schemas import (
    RegisterForm,
    UserResponse,
    TokenResponse,
    LoginForm,
)


auth_router = APIRouter()


@auth_router.post(
    "/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    register_form: RegisterForm,
    auth_service: AbstractAuthService = Depends(get_auth_service),
) -> UserResponse:
    if register_form.password != register_form.confirm_password:
        raise PasswordsNotMatch
    user = await auth_service.registration_new_user(
        register_form.email, register_form.password
    )
    return user


@auth_router.post(
    "/login/", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def login(
    request: Request,
    login_form: LoginForm,
    auth_service: AbstractAuthService = Depends(get_auth_service),
    jwt_service: AbstractJWTService = Depends(get_jwt_service),
) -> TokenResponse:
    user = await auth_service.login_user(
        email=login_form.email, password=login_form.password
    )
    access_token = jwt_service.generate_access_token(user)
    refresh_token = jwt_service.generate_refresh_token(user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# @auth_router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
# async def logout(
#     token_data: Token = Depends(get_token_data),
#     black_list_service: AbstractBlackListService = Depends(get_black_list_service),
# ) -> None:
#     pass


# @auth_router.post("/change-password/")
# async def change_password():
#     pass
