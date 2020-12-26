from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIME

from .database import Base

class CourseSession(Base):
    __tablename__ = "course_session"

    crn = Column(VARCHAR(length=255))
    section = Column(VARCHAR(length=255))
    semester = Column(VARCHAR(length=255))
    time_start = Column(TIME)
    time_end = Column(TIME)
    day_of_week = Column(INTEGER)
    location = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('crn', 'section', 'semester', 'day_of_week'),
    )