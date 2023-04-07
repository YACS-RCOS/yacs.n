from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Professor(Base):
    __tablename__ = "professor"

    email = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    first_name = Column(VARCHAR(length=255))
    last_name = Column(VARCHAR(length=255)) 
    phone_number = Column(VARCHAR(length=255)) 
    department = Column(VARCHAR(length=255))
    office_room = Column(VARCHAR(length=255))
    #classes = Column(VARCHAR(length=255), ForeignKey("course.crn")) 
    classes = Column(VARCHAR(length=255)) 
    office_hours_time = Column(VARCHAR(length=255))
    rcs = Column(VARCHAR(length=255))
