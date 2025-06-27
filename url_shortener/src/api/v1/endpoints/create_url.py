import logging

from fastapi import APIRouter, status

from src.api.v1.dedpendencies import short_urlDep
from src.api.v1.schemas import CreateUrlRequest, CreateUrlResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/create",
    response_model=CreateUrlResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание сокращённой ссылки"
)
async def create_url(
    create_url: CreateUrlRequest,
    service: short_urlDep,
) -> CreateUrlResponse:
    create_url_response = await service.create_short_url(create_url.url)
    return CreateUrlResponse(short_url=create_url_response)
