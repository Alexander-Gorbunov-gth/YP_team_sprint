from fastapi import APIRouter
from src.api.v1.endpoints.events import router as events_router
from src.api.v1.endpoints.profile import router as profile_router
from src.api.v1.endpoints.subscribe import router as subscribe_router
from src.api.v1.endpoints.booking import router as booking_router
from src.api.v1.endpoints.evaluations import router as evaluations_router

router = APIRouter(prefix="/v1")


router.include_router(events_router)
router.include_router(profile_router)
router.include_router(subscribe_router)
router.include_router(booking_router)
router.include_router(evaluations_router)
