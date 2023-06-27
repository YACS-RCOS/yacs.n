from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR

from .database import Base

class Cateogry_name(Base):
    __tablename__ = "category_name"

    name = Column(VARCHAR(length=255), primary_key = True, nullable=False)