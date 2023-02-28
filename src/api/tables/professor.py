from pickle import TRUE
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TSVECTOR

from .database import Base

class Professor(Base):
    __tablename__ = "professor"

    first_name = Column(VARCHAR(length=255))
    last_name = Column(VARCHAR(length=255)) 
    #optional phone number
    phone_number = Column(VARCHAR(length=255)) 
    email = Column(VARCHAR(length=255), primary_key = TRUE)
    department = Column(VARCHAR(length=255))
    office_room = Column(VARCHAR(length=255))
    classes = Column(VARCHAR(length=255), ForeignKey('course.crn')) #maybe TSVECTOR
    office_hours_time = Column(TSVECTOR)
    webex = Column(VARCHAR(length=255))