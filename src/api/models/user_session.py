from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, UUID


class UserSession(Base):
    __tablename__ = "user_session"

    session_id = fields.IntField(pk=True)
    user_id = fields.IntField(nullable=False)
    # start_time = Column(TIMESTAMP(timezone=True))
    start_time = fields.DatetimeField()
    # end_time = Column(TIMESTAMP(timezone=True))
    end_time = fields.DatetimeField()

    class Meta:
        table = "user_session"