from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Professor(Base):
    __tablename__ = "professor"

    email = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    name = Column(VARCHAR(length=255), nullable=True)
    title = Column(VARCHAR(length=255), nullable=True)
    phone_number = Column(VARCHAR(length=255),nullable=True) 
    department = Column(VARCHAR(length=255), nullable=True)
    portfolio_page = Column(VARCHAR(length=255),nullable=True)
    office_room = Column(VARCHAR(length=255), nullable=True)
    classes = Column(VARCHAR(length=255), ForeignKey("course.crn")) 
    office_hours_time = Column(VARCHAR(length=255), nullable=True)
    rcs = Column(VARCHAR(length=255), nullable = True)
