from tortoise import fields
from tortoise.models import Model


class UserAccount(Model):
    user_id = fields.IntField(pk=True)
    name = fields.TextField(null=True)
    email = fields.CharField(nullable=False, unique=True, max_length=255)
    phone = fields.TextField(null=True)
    password = fields.TextField(null=True)
    major = fields.TextField(null=True)
    degree = fields.TextField(null=True)
    enable = fields.BooleanField(default=True, null=True)
    admin = fields.BooleanField(default=False, null=True)
    super_admin = fields.BooleanField(default=False, null=True)

    class Meta:
        table = "user_account"