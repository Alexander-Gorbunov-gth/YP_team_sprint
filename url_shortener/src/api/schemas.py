from pydantic import BaseModel, HttpUrl, Field


class GetUrlResponse(BaseModel):
    url: HttpUrl = Field(..., description="Оригинальная ссылка")
