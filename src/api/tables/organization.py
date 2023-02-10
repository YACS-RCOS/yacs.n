from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, TIME

from .database import Base

class ClubInfo(Base):
    __tablename__ = "Organization Info"

    org_id = Column(VARCHAR(length=7))
    name = Column(VARCHAR(length=255))
    location = Column(VARCHAR(length=255))
    size = Column(VARCHAR(length=255))
    operation = Column(BOOLEAN, default=True)
    day_of_week = Column(INTEGER)
    meeting_time = Column(VARCHAR(length=255))
    contact = Column(VARCHAR(length=255))
    leader = Column(VARCHAR(length=255))
    focus_type = Column(VARCHAR(length=255))
    organization_type = Column(VARCHAR(length=255))
    requirement = Column(VARCHAR(length=255))
    discription = Column(VARCHAR(length=255))  
    new_member = Column(BOOLEAN, default=True)

    __table_args__ = (
        PrimaryKeyConstraint('org_id'),
    )