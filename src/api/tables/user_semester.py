
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, FLOAT

from .database import Base

class UserSemesters(Base):
	__tablename__ = "user_semesters"

	user_id = Column(INTEGER, primary_key=True)
	semester = Column(TEXT)
	courses = Column(TEXT)
	GPA = Column(FLOAT)