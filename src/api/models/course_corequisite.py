from tortoise import fields
from tortoise.models import Model

class CourseCorequisite(Model):

    department = fields.IntField(length=255)
    level = fields.IntField()
    corequisite = fields.IntField(length=255)

    class Meta:
        table = "course_corequisite"
        unique_together = (('department', 'level', 'corequisite'),)