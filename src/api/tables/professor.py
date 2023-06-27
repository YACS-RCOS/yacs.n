from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Professor(Base):
    __tablename__ = "professor"

    Email = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    Name = Column(VARCHAR(length=255), nullable = True) #try changign datatype to stirng
    Title = Column(VARCHAR(length=255), nullable=True)
    Phone_number = Column(VARCHAR(length=255), nullable=True) 
    Department = Column(VARCHAR(length=255), nullable=True)
    Portfolio_page = Column(VARCHAR(length=255), nullable=True)
    Profile_page = Column(VARCHAR(length=255), nullable=True)

    # rcs = Column(VARCHAR(length=255), nullable = True)
