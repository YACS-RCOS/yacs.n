from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255))
    description = Column(TEXT)
    category = Column(VARCHAR(length=255))
    # required_courses = Column(TSVECTOR, bool = False)
    # #foreign key for courses
    # courses = Column(TSVECTOR, foreign_key = TRUE)
    