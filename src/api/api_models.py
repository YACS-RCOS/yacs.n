from pydantic import BaseModel
from typing import Optional

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class UserPydantic(BaseModel):
     name: str
     email: str
     phone: str
     password: str
     major: str
     degree: str

class UserDeletePydantic(BaseModel):
    sessionID: str
    password: str


