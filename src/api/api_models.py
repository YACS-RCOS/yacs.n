from pydantic import BaseModel
from typing import Optional


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
    newPassword:str
    major:str
    degree:str

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

class UserCoursePydantic(BaseModel):
    name: str
    semester: str
    cid: str

class SubsemesterPydantic(BaseModel):
    semester: Optional[str] = None

class DefaultSemesterSetPydantic(BaseModel):
    default: str

class ProfessorPydantic(BaseModel):
    email: str
    first_name: str
    last_name: str 
    phone_number: str 
    department: str 
    office_room: str 
    classes: str
    office_hours_time: str 
    rcs: str
#add professor and figure out what to do
    
