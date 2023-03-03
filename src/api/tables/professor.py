from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TSVECTOR

from .database import Base

class Professor(Base):
    __tablename__ = "professor"

    first_name = Column(VARCHAR(length=255))
    last_name = Column(VARCHAR(length=255)) 
    phone_number = Column(VARCHAR(length=255)) 
    email = Column(VARCHAR(length=255), primary_key = True)
    department = Column(VARCHAR(length=255))
    office_room = Column(VARCHAR(length=255))
    #ForeignKey('user_account.user_id')
    classes = Column(TSVECTOR, ForeignKey("course.crn")) 
    office_hours_time = Column(TSVECTOR)
    webex = Column(VARCHAR(length=255))
