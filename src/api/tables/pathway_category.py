from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class pathway_category(Base):
    __tablename__ = "pathway_category"

    category_name = Column(VARCHAR(length=255), primary_key = True, nullable=False)

