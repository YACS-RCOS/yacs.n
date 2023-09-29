from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class pathway_field(Base):
    __tablename__ = "pathway_field"

    pathway_name = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    field_number = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    occurance = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    course_credits = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    course_level = Column(VARCHAR(length=255), primary_key = True, nullable=False)
    desc_credit_level = Column(VARCHAR(length=255), primary_key = True, nullable=False)

