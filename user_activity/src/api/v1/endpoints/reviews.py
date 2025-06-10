from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/")
async def create_review():
    pass


@router.get("/")
async def get_reviews_by_film_id():
    pass


@router.get("/")
async def get_reviews_by_user_id():
    pass


@router.get("/{like_id}")
async def get_review_by_id():
    pass


@router.patch("/{like_id}")
async def update_review():
    pass


@router.delete("/{like_id}")
async def delete_review():
    pass
