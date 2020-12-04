from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, DATE

from database import Base

class SemesterDateRange(Base):
    __tablename__ = 'semester_date_range'

    semester_part_name = Column(VARCHAR(length=255))
    date_start = Column(DATE)
    date_end = Column(DATE)

    __table_args__ = (
        PrimaryKeyConstraint('date_start', 'date_end'),
    )