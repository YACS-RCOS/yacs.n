from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR 

from .database import Base

class rmp(Base):
    __tablename__ = "course"

    tDept = Column(VARCHAR(length=255))
    tSid = Column(INTEGER)
    institution_name = Column(VARCHAR(length=255))
    tFname = Column(VARCHAR(length=255))
    tMiddlename = Column(VARCHAR(length=255))
    tLname = Column(VARCHAR(length=255))
    tid = Column(INTEGER)
    tNumRatings = Column(INTEGER)
    rating_class = Column(VARCHAR(length=255))
    contentType = Column(VARCHAR(length=255))
    categoryType = Column(VARCHAR(length=255))
    overall_rating = Column(Decimal(2,1)) #can change to integer later on