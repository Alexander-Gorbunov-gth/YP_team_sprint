from uuid import UUID

from domain.templates import Template
from jinja2 import Environment
from jinja2 import Template as JinjaTemplate
from jinja2 import TemplateSyntaxError, meta
from src.infrastructure.models import TemplateModel
from src.services.interfaces.repositories.template import AbstractTemplateRepository
from src.services.interfaces.services.template import AbstractTemplateService


class TemplateService(AbstractTemplateService):
    def __init__(self, template_repository: AbstractTemplateRepository):
        self._template_repository = template_repository

    @staticmethod
    def _get_template_model(template: TemplateModel) -> Template:
        return Template(
            id=template.id,
            event_type=template.name,
            subject=template.subject,
            body=template.template,
        )

    async def get_template(self, template_id: UUID) -> Template:
        """
        Получает шаблон по id
        :param template_id: UUID шаблона
        :return: модель шаблона
        """
        template = await self._template_repository.get_template(template_id=template_id)
        return self._get_template_model(template=template)

    async def get_template_by_name(self, name: str) -> Template:
        """
        Получает шаблон по имени
        :param name: имя шаблона
        :return: модель шаблона
        """

        template = await self._template_repository.get_template_by_name(name=name)
        return self._get_template_model(template=template)

    async def preview_template(self, template_id: UUID) -> str:
        """
        Предварительный просмотр шаблона заполняя все переменные
        :param template_id: UUID шаблона
        :return: строка с предварительным просмотром шаблона
        """

        template = self._get_template_model(await self.get_template(template_id=template_id))
        env = Environment()
        template = JinjaTemplate(template.body)
        parsed_template = env.parse(template.body)
        variables = meta.find_undeclared_variables(parsed_template)
        context = {}
        for variable in variables:
            context[variable] = variable
        try:
            html_template = template.render(**context)
        except Exception as e:
            raise TemplateSyntaxError(f"Ошибка при предварительном просмотре шаблона: {e}")
        return html_template
