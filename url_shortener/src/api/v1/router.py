from fastapi import APIRouter
from src.api.v1.endpoints.create_url import router as create_url_router

router = APIRouter(prefix="/v1")

router.include_router(create_url_router)
