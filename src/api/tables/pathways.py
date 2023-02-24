from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT

from .database import Base

class Pathway(Base):
    __tablename__ = "pathway"

    name = Column(VARCHAR(length=255), nullable=False)
    description = Column(TEXT)
    category = Column(VARCHAR(length=255))
    #make this a table and link it to requiremetns
    