from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, UUID

from .database import Base

class UserSession(Base):
    __tablename__ = "user_session"

    session_id = Column(UUID, primary_key=True)
    user_id = Column(INTEGER, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))