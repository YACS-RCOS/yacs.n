from tkinter.tix import TEXT
from tokenize import String
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

from .database import Base

class MajorTemplate(Base):
    __tablename__ = "major_templates_2022"

    Major = Column(TEXT)
    Year = Column(TEXT)
    Semester = Column(TEXT)
    Courses = Column(ARRAY(TEXT))
    
    
    
    


    __table_args__ = (
        PrimaryKeyConstraint('Major', 'Year', 'Semster'),
    )
