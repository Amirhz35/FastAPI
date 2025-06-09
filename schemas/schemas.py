from pydantic import BaseModel


class URL_Create(BaseModel):
    request_url: str


class URL_Read(BaseModel):
    original_url: str
    short_url: str
