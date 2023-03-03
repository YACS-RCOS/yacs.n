from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, ARRAY

from .database import Base

class degree_templates(Base):
    __tablename__ = "degree_templates"

    major = Column(VARCHAR(length=255), primary_key=True)
    year = Column(INTEGER)
    englishyear = Column(VARCHAR(length=255))
    semester = Column(INTEGER)
    season = Column(VARCHAR(length=255))
    courses = Column(ARRAY(TEXT))
    
    
    
    # section = Column(VARCHAR(length=255))
    # semester = Column(VARCHAR(length=255))
    # min_credits = Column(INTEGER)
    # max_credits = Column(INTEGER)
    # date_start = Column(DATE)
    # date_end = Column(DATE)
    # department = Column(VARCHAR(length=255))
    # level = Column(INTEGER)
    # title = Column(VARCHAR(length=255))
    # full_title = Column(TEXT)
    # description = Column(TEXT)
    # raw_precoreqs = Column(TEXT)
    # frequency = Column(VARCHAR(length=255))
    # school = Column(VARCHAR(length=255))
    # seats_open = Column(INTEGER)
    # seats_filled = Column(INTEGER)
    # seats_total = Column(INTEGER)
    # tsv = Column(TSVECTOR)