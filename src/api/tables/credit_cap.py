from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Credit_Cap(Base):
    __tablename__ = 'credit_cap'

    cap = Column(INTEGER)
    credit_cap_warning = Column(VARCHAR(length=255))