from fastapi import APIRouter

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/")
async def create_like():
    pass


@router.get("/")
async def get_likes_by_film_id():
    pass


@router.get("/")
async def get_likes_by_user_id():
    pass


@router.get("/{like_id}")
async def get_like_by_id():
    pass


@router.delete("/{like_id}")
async def delete_like():
    pass
