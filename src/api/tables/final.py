from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIME

from .database import Base

class Final(Base):
    __tablename__ = "final"

    season = Column(VARCHAR(length=255))
    year = Column(INTEGER)
    major = Column(VARCHAR(length=255))
    course = Column(VARCHAR(length=255))
    section = Column(INTEGER)
    start = Column(TIME)
    end = Column(TIME)
    building = Column(VARCHAR(length=255))
    room = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('major', 'course', 'section', 'season', 'year'),
    )
