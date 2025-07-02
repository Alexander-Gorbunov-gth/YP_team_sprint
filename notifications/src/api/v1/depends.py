from typing import Annotated

from fastapi import Depends
from src.services.depends import Template_Repository_Dep
from src.services.template import TemplateService


def get_template_service(template_repository: Template_Repository_Dep) -> TemplateService:
    return TemplateService(template_repository=template_repository)


Template_Service_Dep = Annotated[TemplateService, Depends(get_template_service)]
