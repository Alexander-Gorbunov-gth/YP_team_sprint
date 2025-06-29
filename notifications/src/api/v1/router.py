from fastapi import APIRouter
from src.api.v1.endpoints.templates import router as templates_router
from src.api.v1.endpoints.websockets import router as websockets_router

router = APIRouter(prefix="/v1")


router.include_router(templates_router)
router.include_router(websockets_router)
