from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base


class Professor(Base):
    __tablename__ = "professor"

    email = Column(VARCHAR(length=255), primary_key=True)
    name = Column(VARCHAR(length=255), nullable=True)
    title = Column(VARCHAR(length=255), nullable=True)
    phone_number = Column(VARCHAR(length=255), nullable=True)
    department = Column(VARCHAR(length=255), nullable=True)
    portfolio_page = Column(VARCHAR(length=255), nullable=True)
    profile_page = Column(VARCHAR(length=255), nullable=True)

    # rcs = Column(VARCHAR(length=255), nullable = True)
