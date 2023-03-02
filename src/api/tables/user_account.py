from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BOOLEAN, VARCHAR, TSVECTOR

from .database import Base

class UserAccount(Base):
    __tablename__ = "user_account"

    user_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    email = Column(TEXT, nullable=False, unique=True)
    phone = Column(TEXT)
    password = Column(TEXT)
    major = Column(TEXT)
    degree = Column(TEXT)
    past_classes = Column(TSVECTOR)
    GPA = Column(INTEGER)
    school = Column(VARCHAR(length=255)) #for future purposes
    semester = Column(VARCHAR(length=255))
    enable = Column(BOOLEAN, default=True)
    admin = Column(BOOLEAN, default=False)
    super_admin = Column(BOOLEAN, default=False)