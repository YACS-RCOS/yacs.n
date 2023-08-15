from sqlalchemy import Column, ForeignKey, String, Integer
from sqalchemy import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from .database import Base

class Course(Base):
    __tablename__ = "courses"

    #crn = Column(VARCHAR(length=255), primary_key=True)
    #section = Column(VARCHAR(length=255))
    #semester = Column(VARCHAR(length=255))
    #min_credits = Column(INTEGER)
    #max_credits = Column(INTEGER)
    #date_start = Column(DATE)
    #date_end = Column(DATE)
    #department = Column(VARCHAR(length=255))
    #level = Column(INTEGER)
    #title = Column(VARCHAR(length=255))
    #full_title = Column(TEXT)
    #description = Column(TEXT)
    #raw_precoreqs = Column(TEXT)
    #frequency = Column(VARCHAR(length=255))
    #school = Column(VARCHAR(length=255))
    #seats_open = Column(INTEGER)
    #seats_filled = Column(INTEGER)
    #seats_total = Column(INTEGER)
    #tsv = Column(TSVECTOR)

    id = Column(Integer, primary_key=True)
    pathway_id = Column(Integer, ForeignKey('pathways.id'))
    name = Column(String)
    pathway = relationship("Pathway", back_populates="courses")