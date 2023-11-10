from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from .database import Base
# from .database import Base
import json


class CoursesMaster():
    __tablename__ = "courses_master"

    min_credits = Column(INTEGER, primary_key=True, nullable=False)##KEY
    max_credits = Column(INTEGER, primary_key=True, nullable=False)##KEY
    department = Column(VARCHAR(length=255), primary_key=True, nullable=False)##KEY
    level = Column(INTEGER, primary_key=True, nullable=False)##KEY
    title = Column(VARCHAR(length=255), primary_key=True, nullable=False)##KEY

    full_title = Column(TEXT, primary_key=False, nullable=True)
    raw_precoreqs = Column(TEXT, primary_key=False, nullable=True)
    school = Column(VARCHAR(length=255), primary_key=False, nullable=True)
