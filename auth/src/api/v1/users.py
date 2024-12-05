from fastapi import APIRouter, Depends


users_router = APIRouter()


@users_router.get("/")
async def get_all_users():
    pass

@users_router.post("/")
async def create_user():
    pass


@users_router.get("/{uuid}/")
async def get_user():
    pass


@users_router.patch("/{uuid}/")
async def change_user():
    pass


@users_router.patch("/{uuid}/change-permissions/")
async def add_permission():
    """Здесь предлагаю сделать один метод который 
    будет принимать массив из словарей 
    тип: какое разрешение
    действие: добавить или убрать 
    """
    pass

