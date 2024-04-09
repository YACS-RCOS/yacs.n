from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    category_name = Column(VARCHAR(length=255))
    pathways_name = Column(VARCHAR(length=255))
    description = TEXT
    required_courses = Column(TSVECTOR, bool = False)
    #description and list of courses for reuqired_courses
    #foreign key for courses
    courses = Column(TSVECTOR, ForeignKey("course.crn"))
    compatible_minor = Column(TSVECTOR)

    # [Arts/Design[Creative Design, Grahpic], ]
