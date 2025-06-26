from datetime import datetime
from typing import Dict, List
from uuid import UUID
from pydantic import BaseModel

from src.domain.channels import ChannelLiteral


class Client(BaseModel):
    id: UUID
    name: str
    email: str
    active_channels: list[ChannelLiteral]


class ClientsData(BaseModel):
    data: list[Client]