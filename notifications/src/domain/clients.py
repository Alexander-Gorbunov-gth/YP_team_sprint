from datetime import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel
from src.domain.channels import ChannelLiteral, ChannelTypes


class Client(BaseModel):
    id: UUID
    name: str
    email: str
    timezone: str
    active_channels: list[ChannelLiteral]
    ip: str | None = "some_ip"

    def get_address(self, channel: ChannelLiteral) -> str:
        """Получает адрес клиента для указанного канала."""
        if channel == ChannelTypes.EMAIL:
            return self.email
        if channel == ChannelTypes.PUSH:
            return f"push:{self.ip}"
        raise ValueError(f"Неизвестный канал: {channel}. Поддерживаются только {list(ChannelTypes)}.")
