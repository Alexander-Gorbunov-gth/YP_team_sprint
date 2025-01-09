from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class IModel(ABC):
    """
    Базовая абстрактная модель.
    Предназначена для наследования другими моделями в доменной логике.
    """

    async def to_dict(
        self, exclude: tuple[str] | None = None, include: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Преобразует объект модели в словарь.

        Args:
            exclude (tuple[str] | None, optional): Набор полей, которые нужно исключить из словаря. По умолчанию None.
            include (dict[str, Any] | None, optional): Дополнительные поля, которые нужно включить
            или заменить в словаре. По умолчанию None.

        Returns:
            dict[str, Any]: Словарь, представляющий объект модели.
        """

        data: dict[str, Any] = asdict(self)
        if exclude is not None:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include is not None:
            data.update(include)

        return data
