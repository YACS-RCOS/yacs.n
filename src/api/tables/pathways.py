from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR, BOOLEAN

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255))
    description = TEXT
    #change srcture
    required_courses = Column(TSVECTOR, bool = False)
    #foreign key for courses
    courses = Column(TSVECTOR)
    compatible_minor = Column(TSVECTOR)
#each pahtways has a category name
#degree_sturctions