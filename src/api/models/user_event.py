from tortoise import fields
from tortoise import UUID
from tortoise.models import Model

class UserEvent(Model):
    # __tablename__ = "user_event"

    event_id = fields.IntField()
    user_id = fields.UUIDField()
    content = fields.TextField()
    created_at = fields.BigIntField()
    class Meta:
        table = "user_event"
        unique_together=(("event_id","user_id"),)