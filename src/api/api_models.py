from pydantic import BaseModel
from typing import Optional
from typing import List


class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class CourseDeletePydantic(BaseModel):
    name: str
    cid: Optional[str] = None
    semester: str


class updateUser(BaseModel):
    name:str
    sessionID:str
    email:str
    phone:str
    password:str
    newpassword:Optional[str] = None
    major: List[str]
    degree:str

class UserPydantic(BaseModel):
     name: str
     email: str
     phone: str
     password: str
     major: List[str]
     degree: str

class UserDeletePydantic(BaseModel):
    sessionID: str
    password: str

class UserCoursePydantic(BaseModel):
    name: str
    semester: str
    cid: str

class SubsemesterPydantic(BaseModel):
    semester: Optional[str] = None

class DefaultSemesterSetPydantic(BaseModel):
    default: str