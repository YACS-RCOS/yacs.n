from tortoise import fields
from tortoise.models import Model

class AdminSettings(Model):

    semester = fields.CharField(pk=True,unique=True, max_length=255)
    class Meta:
        table = 'admin_settings'