from tortoise import fields
from tortoise.models import Model


class Event(Model):
    event_id = fields.IntField(pk=True)
    description = fields.CharField(max_length=255)

    class Meta:
        table = 'event'
