from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, BOOLEAN

from .database import Base

class SemesterInfo(Base):
    __tablename__ = "semester_info"

    semester = Column(VARCHAR(length=255), primary_key=True)
    public = Column(BOOLEAN)

    courses = relationship(
        "Course",
        back_populates="semester_info",
        cascade="all, delete",
        passive_deletes=True,
    )