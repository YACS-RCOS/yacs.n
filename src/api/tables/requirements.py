from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TSVECTOR, VARCHAR

from .database import Base

class Requirements(Base):
    __tablename__ = "requirements"

    name = Column(VARCHAR(length=255))
    pathways = Column(TSVECTOR)
    classes_provded = Column(TSVECTOR)
