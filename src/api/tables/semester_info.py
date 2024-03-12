from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, BOOLEAN

from .database import Base

class SemesterInfo(Base):
    __tablename__ = "semester_info"

    semester = Column(VARCHAR(length=255), primary_key=True)
    public = Column(BOOLEAN)
