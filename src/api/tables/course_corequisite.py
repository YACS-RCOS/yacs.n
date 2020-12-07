from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from .database import Base

class CourseCorequisite(Base):
    __tablename__ = 'course_corequisite'

    department = Column(VARCHAR(length=255))
    level = Column(INTEGER)
    corequisite = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('department', 'level', 'corequisite'),
    )