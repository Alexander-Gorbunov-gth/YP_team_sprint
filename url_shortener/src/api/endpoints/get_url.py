import logging

from fastapi import APIRouter, status, Path

from src.api.dedpendencies import short_urlDep
from src.api.schemas import GetUrlResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/{url}",
    response_model=GetUrlResponse,
    status_code=status.HTTP_200_OK,
    summary="Получение оригинальной ссылки"
)
async def get_url(
    service: short_urlDep,
    url: str = Path(..., description="Сокращённая ссылка"),
) -> GetUrlResponse:
    get_url_response = await service.get_original_url(url)
    return GetUrlResponse(url=get_url_response)
