from fastapi import APIRouter


me_router = APIRouter()


@me_router.get("/{uuid}")
async def my_profile():
    pass


@me_router.get("/{uuid}/sessions/")
async def my_sessions():
    pass
