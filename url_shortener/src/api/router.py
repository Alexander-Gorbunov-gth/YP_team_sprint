from fastapi import APIRouter
from src.api.v1.router import router as v1_router
from src.api.endpoints.get_url import router as _original_router

router = APIRouter(prefix="/api")
original_router = APIRouter()

router.include_router(v1_router)
original_router.include_router(_original_router)
