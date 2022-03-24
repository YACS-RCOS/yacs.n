from pydantic import BaseModel
from typing import Optional

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class UserCoursePydantic(BaseModel):
    # email: str
    # password: str
    name: str
    semester: str
    user_id: str
    cid: str

