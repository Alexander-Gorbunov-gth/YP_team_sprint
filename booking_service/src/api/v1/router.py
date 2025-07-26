from fastapi import APIRouter

from src.api.v1.endpoints.address import router as address_router
from src.api.v1.endpoints.evaluations import router as evaluations_router
from src.api.v1.endpoints.events import router as events_router
from src.api.v1.endpoints.reservation import router as reservation_router
from src.api.v1.endpoints.subscribe import router as subscribe_router

router = APIRouter(prefix="/v1")


router.include_router(events_router)
router.include_router(subscribe_router)
router.include_router(reservation_router)
router.include_router(evaluations_router)
router.include_router(address_router)
