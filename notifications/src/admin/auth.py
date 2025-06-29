from sqladmin.authentication import AuthenticationBackend
from src.core.config import settings
from starlette.requests import Request


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")
        if email == settings.admin.email and password == settings.admin.password:
            request.session.update({"token": settings.admin.token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return token == settings.admin.token
