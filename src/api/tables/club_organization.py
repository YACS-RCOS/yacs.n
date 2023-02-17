from tkinter.tix import TEXT
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import DATE, VARCHAR, TSVECTOR

from .database import Base

class Club(Base):
    __tablename__ = "club"

    name = Column(VARCHAR(length=255))
    description = Column(TEXT)
    building = Column(VARCHAR(length=255))
    room = Column(VARCHAR(length=255))
    days = Column(TSVECTOR)
    start = Column(DATE)
    end = Column(DATE)