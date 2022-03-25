from pydantic import BaseModel

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


