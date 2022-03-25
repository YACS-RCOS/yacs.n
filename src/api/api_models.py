from pydantic import BaseModel
from typing import Optional

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str


class updateUser(BaseModel):
    name:str
    sessionID:str
    email:str
    phone:str
    newPassword:str
    major:str
    degree:str
