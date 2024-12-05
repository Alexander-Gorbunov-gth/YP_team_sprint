from fastapi import APIRouter, Depends


auth_router = APIRouter()




@auth_router.post("/register/")
async def register():
    pass


@auth_router.post("/login/")
async def login():
    pass



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
