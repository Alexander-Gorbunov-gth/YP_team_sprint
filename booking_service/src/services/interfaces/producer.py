import abc
from datetime import datetime
from typing import Dict
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.channels import ChannelLiteral


class PublishMessage(BaseModel):
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
    user_params: Dict[UUID, Dict[str, str]] | None = Field(
        None,
        description="Данные клиентов для отправки",
        example={"user_uuid": {"key1": "value1", "key2": "value2"}},
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


class IProducer(abc.ABC):
    @abc.abstractmethod
    async def publish(self, message: PublishMessage) -> None: ...
