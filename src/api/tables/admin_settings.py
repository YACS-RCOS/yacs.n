from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class AdminSettings(Base):
    __tablename__ = 'admin_settings'

    semester = Column(VARCHAR(length=255), primary_key=True, unique=True)