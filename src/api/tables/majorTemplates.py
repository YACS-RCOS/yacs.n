from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, ARRAY

from .database import Base

class MajorTemplates(Base):
    __tablename__ = "majorTemplates"

    Major = Column(TEXT, nullable=False)
    Year = Column(TEXT, nullable=False)
    Semester = Column(TEXT, nullable=False)
    Courses = Column(ARRAY(TEXT))