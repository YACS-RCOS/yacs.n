from tortoise import fields
from tortoise.models import Model


class UserAccount(Model):
    user_id = fields.IntField(pk=True)
    name = fields.TextField()
    email = fields.CharField(nullable=False, unique=True, max_length=255)
    phone = fields.TextField()
    password = fields.TextField()
    major = fields.TextField()
    degree = fields.TextField()
    enable = fields.BooleanField(default=True)
    admin = fields.BooleanField(default=False)
    super_admin = fields.BooleanField(default=False)

    class Meta:
        table = "user_account"