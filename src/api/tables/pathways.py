from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR

from .course import Course
from connection import db
from .database import Base

class Pathway(Base):
    __tablename__ = "pathways"

    #name = Column(VARCHAR(length=255), primary_key=True)
    #description = Column(TEXT)
    #compatible_minor = Column(VARCHAR(length=255))
    #category_name = Column(VARCHAR(length=255), ForeignKey('categories.name'))

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String)
    category = relationship("Category", back_populates="pathways")
    courses = relationship("Course", back_populates="pathway")

    #category_name = Column(VARCHAR(length=255), ForeignKey('categories.name'))
    #category = relationship("Category", back_populates="pathways")

   

   