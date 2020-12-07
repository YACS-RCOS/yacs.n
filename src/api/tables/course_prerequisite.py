from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .database import Base

class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisite"

    department = Column(VARCHAR(length=255))
    level = Column(INTEGER)
    prerequisite = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('department', 'level', 'prerequisite'),
    )

