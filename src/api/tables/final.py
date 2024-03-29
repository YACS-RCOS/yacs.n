from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, TIME

from .database import Base

class Final(Base):
    __tablename__ = "finals"

    crn = Column(VARCHAR(length=255), primary_key=True)
    department = Column(VARCHAR(length=255))
    level = Column(INTEGER)
    section = Column(VARCHAR(length=255))
    title = Column(VARCHAR(length=255))
    full_title = Column(TEXT)
    location = Column(TEXT)
    day = Column(INTEGER)
    start_time = Column(TIME)
    end_time = Column(TIME)
