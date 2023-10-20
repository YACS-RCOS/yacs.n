from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from .database import Base


class PathwayMinors(Base):
    __tablename__ = "pathway_minors"

    minor = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    pathway = Column(VARCHAR(length=255), primary_key=True, nullable=False)