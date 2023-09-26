from click import INT
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import VARCHAR

from .database import Base

class Finals(Base):
    __tablename__ = "finals"

    department = Column(VARCHAR(length=255), nullable=False)
    courseCode = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    section = Column(INT, primary_key=True, nullable=False)
    room = Column(VARCHAR(length=255), nullable=False)
    dayOfWeek = Column(VARCHAR(length=255), nullable=False)
    day = Column(VARCHAR(legnth=255), nullable=False)
    hour = Column(VARCHAR(length=255), nullable=False)


    

    # rcs = Column(VARCHAR(length=255), nullable = True)
