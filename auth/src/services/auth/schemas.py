from pydantic import BaseModel


class ResponseTokens(BaseModel):
    refresh_token: str
    access_token: str
    tokens_type: str
