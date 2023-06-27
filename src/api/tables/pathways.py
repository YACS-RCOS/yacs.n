from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TSVECTOR

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255))
    #description = TEXT
    required_courses = Column(TSVECTOR, bool = False)
    #foreign key for courses
    remaining_courses = Column(TSVECTOR, ForeignKey("course.crn"))
    compatible_minor = Column(TSVECTOR, bool = False)
    
    #check out back_populate 