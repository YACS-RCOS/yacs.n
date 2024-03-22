from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .database import Base

class StudentCourseSelection(Base):
    __tablename__ = "student_course_selection"

    user_id = Column(INTEGER, ForeignKey('user_account.user_id'))
    semester = Column(VARCHAR(length=255))
    course_name = Column(VARCHAR(length=255))
    crn = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'semester', 'course_name', 'crn'),
    )
