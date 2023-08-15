from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from pathways import Pathway
from connection import db
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    name = Column(String, primary_key=True)

    #name = Column(VARCHAR(length=255), primary_key=True)
    
    
    #pathways = relationship("Pathway", back_populates="category")
 

   