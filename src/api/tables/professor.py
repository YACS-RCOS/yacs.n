from sqlalchemy import Column
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
    #make classes a foreign key (vecotr of courses)
    classes = Column(TSVECTOR) 
    office_hours_time = Column(TSVECTOR)
    webex = Column(VARCHAR(length=255))
