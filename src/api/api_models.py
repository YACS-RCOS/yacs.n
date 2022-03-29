from pydantic import BaseModel

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class CourseDeletePydantic(BaseModel):
    course_name: str
    cid: str
    semester: str


