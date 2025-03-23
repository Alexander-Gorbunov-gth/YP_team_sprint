from fastapi import APIRouter

from src.api.v1.auth import auth_router
from src.api.v1.me import me_router
from src.api.v1.oauth import oauth_router
from src.api.v1.permission import perm_router
from src.api.v1.roles import roles_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(me_router, prefix="/me", tags=["me"])
v1_router.include_router(roles_router, prefix="/roles", tags=["roles"])
v1_router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
v1_router.include_router(perm_router, prefix="/permissions", tags=["permissions"])
