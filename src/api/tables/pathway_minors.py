from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class pathway_minors(Base):
    __tablename__ = "pathway_minors"

    pathway = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    minor  = Column(VARCHAR(length=255), primary_key = True, nullable=False)

