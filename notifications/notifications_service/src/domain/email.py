from datetime import datetime
from typing import Dict
from uuid import UUID


from pydantic import BaseModel, ConfigDict, Field


class EmailSendMessage(BaseModel):

    email: str = Field(
        ...,
        description="Email адрес получателя",
    )
    body: str = Field(
        ...,
        description="Тело письма",
    )
    subject: str = Field(
        ...,
        description="Тема письма",
    )
    delay: int = Field(
        0,
        description="Задержка отправки письма в секундах. Если 0, то письмо отправляется немедленно",
    )
