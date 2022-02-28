from pydantic import BaseModel

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str

class EventPostPydantic(BaseModel):
    pass

class UserCoursePydantic(BaseModel):
    email: str
    password: str
    name: str
    user_id: int
    cid: int

