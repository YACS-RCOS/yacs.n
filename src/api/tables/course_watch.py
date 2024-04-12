from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY, INTEGER

from .database import Base

class CourseWatch(Base):
    __tablename__ = "course_watch"

    crn = Column(VARCHAR(length=255), primary_key=True)
    watchers = Column(ARRAY(INTEGER))
