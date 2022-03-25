from pydantic import BaseModel
from typing import Optional

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class UserCoursePydantic(BaseModel):
    name: str
    semester: str
    cid: str

