from sqalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, DATE, TSVECTOR

from .database import Base

class Category(Base):
    __tablename__ = "Category"

    name = Column(VARCHAR(length=255), primary_key=True)
    