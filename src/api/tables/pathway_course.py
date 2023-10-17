from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from .database import Base


class PathwayCourses(Base):
    __tablename__ = "courses"

    dept_code = Column(VARCHAR(length=4), primary_key=True, nullable=False)
    course_code = Column(VARCHAR(length=4), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
