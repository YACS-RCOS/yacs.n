from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BOOLEAN

from .database import Base

class UserAccount(Base):
    __tablename__ = "user_account"

    user_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    email = Column(TEXT, nullable=False, unique=True)
    phone = Column(TEXT)
    password = Column(TEXT)
    major = Column(TEXT)
    degree = Column(TEXT)
    enable = Column(BOOLEAN, default=True)
    admin = Column(BOOLEAN, default=False)
    super_admin = Column(BOOLEAN, default=False)
    organiztion_bool = Column(BOOLEAN, default=True)
    organization_id = Column(VARCHAR(length=7))