from pydantic import BaseModel

class SessionPydantic(BaseModel):
    email: str
    password: str

class SessionDeletePydantic(BaseModel):
    sessionID: str


class updateUser:
    name:str
    sessionID:str
    email:str
    phone:str
    newPassword:str
    major:str
    degree:str
