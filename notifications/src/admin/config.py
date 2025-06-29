from sqladmin import Admin
from src.admin.views import TemplateAdmin


async def add_views(admin: Admin) -> None:
    admin.add_view(TemplateAdmin)
