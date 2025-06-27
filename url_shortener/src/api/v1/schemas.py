from pydantic import BaseModel, HttpUrl, Field


class CreateUrlRequest(BaseModel):
    url: HttpUrl = Field(..., description="Оригинальная ссылка")

class CreateUrlResponse(BaseModel):
    short_url: HttpUrl = Field(..., description="Сокращйнная ссылка")
