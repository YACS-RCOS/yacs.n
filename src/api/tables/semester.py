from pickle import TRUE
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Semester(Base):
    __tablename__ = "semester"
    
    student_id = Column(VARCHAR(length=255), ForeignKey('user_account.user_id'))
    class_title = Column(VARCHAR(length=255)) 
    semester = Column(VARCHAR(length=255),) 
    year = Column(VARCHAR(length=255)) 
    letter_grade = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('student_id', 'class_title', 'semester', 'year'),
    )