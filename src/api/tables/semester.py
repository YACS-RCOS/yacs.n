from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TSVECTOR, VARCHAR

from .database import Base

class Semester(Base):
    __tablename__ = "semester"

    major = Column(VARCHAR(length=255))
    year = Column(VARCHAR(length=255))
    school = Column(VARCHAR(length=255))
    semester = Column(VARCHAR(length=255))