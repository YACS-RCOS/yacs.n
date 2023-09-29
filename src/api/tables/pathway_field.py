from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class pathway_field(Base):
    __tablename__ = "pathway_field"

    pathway_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key= True, nullable=False)
    field_number = Column(VARCHAR(length=255), primary_key= False, nullable=False)
    occurrence = Column(VARCHAR(length=255), primary_key= False, nullable=False)
    course_credits = Column(VARCHAR(length=255), primary_key=False, nullable=False)
    desc_credit_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: 12 credits at the...
    desc_course_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: ... 4000 level

