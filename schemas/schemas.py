from pydantic import BaseModel
from typing import Optional

class URL_Create(BaseModel):
    request_url: str


class URL_Read(BaseModel):
    original_url: str
    short_url: str


class User_register(BaseModel):
    username: str
    password: str
    email: str

class User_login(BaseModel):
    username: str
    password: str
    



class TokenPayload(BaseModel):
    sub: Optional[str] = None  
    exp: Optional[int] = None  


class SystemUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None  
    disabled: Optional[bool] = None 