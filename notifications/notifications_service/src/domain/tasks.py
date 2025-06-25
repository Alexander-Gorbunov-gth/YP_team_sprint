from datetime import datetime
from typing import Dict
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .channels import ChannelTypes

ChannelLiteral = Literal[ChannelTypes.EMAIL, ChannelTypes.PUSH]


class TaskMessage(BaseModel):

    event_type: str = Field(
        ...,
        description="Тип события, например 'send_notification'",
    )
    channels: list[ChannelLiteral] = Field(
        ...,
        description="Список каналов, допустимые значения: 'email', 'push'",
    )
    for_all_users: bool = Field(
        False,
        description="Флаг, указывающий, что событие для всех пользователей",
    )
    user_uuid: UUID = Field(
        ...,
        description="Уникальный идентификатор клиентв",
    )
    params: Dict[str, str] | None = Field(
        None,
        description="Параметры события, которые могут быть использованы в обработчике",
        example={"key1": "value1", "key2": "value2"},
    )
    send_in_local_time: bool = Field(
        False,
        description="Флаг, указывающий, что время отправки события в локальном времени пользователя",
    )
    send_at: datetime | None = Field(
        None,
        description="Время отправки события. Если None, то событие отправляется немедленно",
        example="2023-10-01T12:00:00Z",
    )
