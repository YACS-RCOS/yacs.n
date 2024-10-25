from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIME

from .database import Base

class Final(Base):
    __tablename__ = "final"

    semester = Column(VARCHAR(length=255))
    course = Column(VARCHAR(length=255))
    section = Column(INTEGER)
    start = Column(TIME)
    end = Column(TIME)
    room_assignment = Column(VARCHAR(length=255))

    __table_args__ = (
        PrimaryKeyConstraint('semester', 'course', 'section', 'start', 'room_assignment'),
    )