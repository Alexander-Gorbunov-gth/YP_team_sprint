from fastapi import APIRouter, Depends


perm_router = APIRouter()


@perm_router.get("/")
async def get_all_permissions():
    pass


@perm_router.get("/{code}/")
async def get_permission():
    pass


@perm_router.post("/")
async def create_permission():
    pass


@perm_router.patch("/{code}/")
async def change_permissions():
    pass