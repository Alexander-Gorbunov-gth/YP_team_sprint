from authlib.integrations.starlette_client import OAuth

from src.core.config import settings


oauth = OAuth()
oauth.register(
    name="yandex",
    client_id=settings.oauth.yandex_client_id,
    client_secret=settings.oauth.yandex_client_secret,
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    client_kwargs={"scope": "login:email login:info"},
)
