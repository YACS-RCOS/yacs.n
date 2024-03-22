from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import BIGINT, INTEGER, VARCHAR, UUID

from .database import Base

class UserEvent(Base):
    __tablename__ = "user_event"

    event_id = Column(INTEGER)
    user_id = Column(UUID)
    content = Column(VARCHAR(length=255))
    created_at = Column(BIGINT)

    __table_args__ = (
        PrimaryKeyConstraint('event_id', 'user_id'),
    )
