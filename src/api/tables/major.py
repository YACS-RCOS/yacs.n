from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, BOOLEAN

from .database import Base

print("hi daddy")

class Major(Base):
    __tablename__ = "major_list"
    
    major = Column(TEXT, primary_key=True)
    b = Column(BOOLEAN)
    m = Column(BOOLEAN)
    d = Column(BOOLEAN)