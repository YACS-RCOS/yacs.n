from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, ARRAY

from .database import Base

class MajorTemplates(Base):
    __tablename__ = "majorTemplates"

    Major = Column(TEXT, primary_key=True)
    Year = Column(TEXT, primary_key=True)
    Semester = Column(TEXT, primary_key=True)
    Courses = Column(ARRAY(TEXT))