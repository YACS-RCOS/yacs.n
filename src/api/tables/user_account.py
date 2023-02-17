from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BOOLEAN

from .database import Base

class UserAccount(Base):
    __tablename__ = "user_account"

    user_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    email = Column(TEXT, nullable=False, unique=True)
    phone = Column(TEXT)
    password = Column(TEXT)
    major = Column(TEXT)
    degree = Column(TEXT)
    enable = Column(BOOLEAN, default=True)
    admin = Column(BOOLEAN, default=False)
    super_admin = Column(BOOLEAN, default=False)

    '''
    SELCET user_account.name, user_semester.semester, user_semester.courses, user_GPA
    FROM user_account
    RIGHT JOIN user_semester
    ON user_semester.user_id=user_account.user_id
    ORDER BY user_account.user_id
    '''