from fastapi import APIRouter

from src.api.v1.endpoints.address import router as address_router
from src.api.v1.endpoints.event_feedback import router as event_feedback_router
from src.api.v1.endpoints.events import router as events_router
from src.api.v1.endpoints.reservation import router as reservation_router
from src.api.v1.endpoints.subscribe import router as subscribe_router
from src.api.v1.endpoints.user_feedback import router as user_feedback_router

router = APIRouter(prefix="/v1")


router.include_router(address_router)
router.include_router(event_feedback_router)
router.include_router(events_router)
router.include_router(reservation_router)
router.include_router(subscribe_router)
router.include_router(user_feedback_router)
