from typing import Annotated

from circuitbreaker import circuit
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from httpx import AsyncClient, HTTPStatusError
from src.core.config import settings
from src.infrastructure.container import AppContainer
from src.services.depends import Template_Repository_Dep
from src.services.template import TemplateService


def get_template_service(template_repository: Template_Repository_Dep) -> TemplateService:
    return TemplateService(template_repository=template_repository)


Template_Service_Dep = Annotated[TemplateService, Depends(get_template_service)]
Http_Client_Dep = Annotated[AsyncClient, Depends(AppContainer.get_http_client)]
Token_Dep = Annotated[str, HTTPBearer()]


@circuit(failure_threshold=3, recovery_timeout=10)
async def get_current_user(http_client: Http_Client_Dep, token: Token_Dep):
    url = settings.auth.service_url
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with http_client as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return await response.json()
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


Current_User_Dep = Annotated[dict, Depends(get_current_user)]
