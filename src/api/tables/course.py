from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from .database import Base

class Course(Base):
    __tablename__ = "course"

    crn = Column(VARCHAR(length=255), primary_key=True)
    section = Column(VARCHAR(length=255))
    semester = Column(VARCHAR(length=255))
    min_credits = Column(INTEGER)
    max_credits = Column(INTEGER)
    date_start = Column(DATE)
    date_end = Column(DATE)
    department = Column(VARCHAR(length=255))
    level = Column(INTEGER)
    title = Column(VARCHAR(length=255))
    full_title = Column(TEXT)
    description = Column(TEXT)
    raw_precoreqs = Column(TEXT)
    frequency = Column(VARCHAR(length=255))
    school = Column(VARCHAR(length=255))
    seats_open = Column(INTEGER)
    seats_filled = Column(INTEGER)
    seats_total = Column(INTEGER)
    tsv = Column(TSVECTOR)
    course_instructor = Column(TEXT)
    email = Column(TEXT)