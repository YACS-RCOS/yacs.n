from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .database import Base

class Event(Base):
    __tablename__ = "event"

    event_id =  Column(INTEGER, primary_key=True)
    description = Column(VARCHAR(length=255))
