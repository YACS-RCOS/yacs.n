from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from .database import Base

class Credit_Cap(Base):
    __tablename__ = 'credit_cap'

    cap = Column(INTEGER, primary_key=True)
    credit_cap_warning = Column(VARCHAR(length=255))