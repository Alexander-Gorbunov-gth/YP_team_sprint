from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

from src.api.v1.dependencies import JWTDep, YandexOAuthDep
from src.api.v1.schemas.auth_schemas import LoginResponse

oauth_router = APIRouter()


@oauth_router.get("/yandex/login")
async def login_with_yandex(oauth_service: YandexOAuthDep):
    url = await oauth_service.get_oauth_url()
    return RedirectResponse(url=url)


@oauth_router.get("/yandex/callback")
async def auth_callback(oauth_service: YandexOAuthDep, jwt_service: JWTDep, code: str = Query(...)):
    user = await oauth_service.create_user_by_social_account(code=code)
    access_token = jwt_service.generate_access_token(user=user)
    refresh_token = jwt_service.generate_refresh_token(user=user)
    return LoginResponse(refresh_token=refresh_token, access_token=access_token)
