from tortoise import fields
from tortoise.models import Model

class CourseCorequisite(Model):

    department = fields.IntField(length=255, pk = True)
    level = fields.IntField(pk = True)
    corequisite = fields.IntField(length=255, pk = True)

    class Meta:
        table = "course_corequisite"