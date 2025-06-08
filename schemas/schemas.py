from pydantic import BaseModel


class URL_schema(BaseModel):
    original_url: str
    short_url: str 

