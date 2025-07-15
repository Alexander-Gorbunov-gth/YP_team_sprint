from fastapi import APIRouter
from src.api.v1.endpoints.bookmark import router as bookmarks_router
from src.api.v1.endpoints.like import router as likes_router
from src.api.v1.endpoints.reviews import router as reviews_router

router = APIRouter(prefix="/v1")


router.include_router(likes_router)
router.include_router(reviews_router)
router.include_router(bookmarks_router)
