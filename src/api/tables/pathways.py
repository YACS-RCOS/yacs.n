from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, TSVECTOR

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    pathway_name = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    category_name = Column(VARCHAR(length=255), nullable=False)
