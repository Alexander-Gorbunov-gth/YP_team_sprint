from markupsafe import Markup
from sqladmin import ModelView
from src.infrastructure.models import TemplateModel


class TemplateAdmin(ModelView, model=TemplateModel):
    name = "Шаблон"
    name_plural = "Шаблоны"
    icon = "fa-solid fa-file-pen"

    column_list = [TemplateModel.name, TemplateModel.channel, TemplateModel.subject, "preview_link"]
    column_labels = {
        TemplateModel.name: "Название",
        TemplateModel.channel: "Канал",
        TemplateModel.template: "Шаблон",
        TemplateModel.subject: "Тема",
        "preview_link": "Предпросмотр",
    }
    column_searchable_list = [TemplateModel.name]
    column_sortable_list = [TemplateModel.name]

    def preview_link(self, obj: TemplateModel, prop: str) -> str:
        url = f"/api/v1/templates/{obj.id}/preview"
        return Markup(f'<a href="{url}" target="_blank">Открыть</a>')

    @property
    def column_formatters(self):
        return {"preview_link": self.preview_link}

    column_formatters_list = column_formatters
    column_formatters_detail = column_formatters
    column_formatters_kwargs = {"is_safe": True}
