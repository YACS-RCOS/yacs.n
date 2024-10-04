from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BOOLEAN

from .database import Base

class Test(Base):
    __tablename__ = "test"

    user_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    email = Column(TEXT, nullable=False, unique=True)
    phone = Column(TEXT)
    password = Column(TEXT, nullable=False)
    major = Column(TEXT)
    degree = Column(TEXT)