from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class BaseEntity:
    def to_dict(self, exclude: set[str]) -> dict[str, Any]:
        """
        Преобразует объект в словарь, исключая указанные поля.

        :param exclude: множество полей, которые нужно исключить
        :return: словарь с данными объекта
        """

        exclude = set(exclude) if exclude else set()
        return {key: value for key, value in asdict(self).items() if key not in exclude}


@dataclass
class ShortUrl(BaseEntity):
    short_url: str
    original_url: str
    expires_at: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
