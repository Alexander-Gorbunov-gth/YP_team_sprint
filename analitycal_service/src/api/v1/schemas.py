from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    token: str
    payload: dict[str, Any]
