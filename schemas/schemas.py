from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime, timezone, timedelta

import re

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
    
class Expire_Time(BaseModel):
    expire_time: datetime

    @field_validator('expire_time', mode='before')
    def validate_time(cls, value):
        if isinstance(value, (int, float)):
            expire_time = datetime.now(timezone.utc) + timedelta(seconds=float(value))
        elif isinstance(value, str):
            regex = r'(?:(\d+)\s*d)?\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?'
            value = value.strip().lower()

            match = re.fullmatch(regex, value)

            # will return with datetime format
            if not match:
                if datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                    raise ValueError("expire_time cannot be in the past")
                return value
            # will return with "1h 2m" format
            groups = match.groups()
            days = int(groups[0]) if groups[0] is not None else 0
            hours = int(groups[1]) if groups[1] is not None else 0
            minutes = int(groups[2]) if groups[2] is not None else 0
            seconds = int(groups[3]) if groups[3] is not None else 0
            
            expire_time = datetime.now(timezone.utc) + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        else:
            raise ValueError("Unsupported type for expire_time")
        
        return expire_time



class TokenPayload(BaseModel):
    sub: Optional[str] = None  
    exp: Optional[int] = None  


class SystemUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None  
    disabled: Optional[bool] = None 