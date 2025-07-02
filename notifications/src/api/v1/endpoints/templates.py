from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse
from src.api.v1.depends import Template_Service_Dep

router = APIRouter(prefix="/templates")


@router.get(
    "/{template_id}/preview",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
    response_model=None,
    summary="Предварительный просмотр шаблона",
)
async def preview_template(template_id: str, template_service: Template_Service_Dep):
    """Предварительный просмотр шаблона"""

    preview_template = await template_service.preview_template(template_id=template_id)
    return HTMLResponse(content=preview_template)
