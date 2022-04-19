from tortoise import fields
from tortoise.models import Model

class SemesterInfo(Model):
    semester = fields.CharField(pk=True,max_length=255)
    public = fields.BoolField(null=True)

    class Meta:
        table = "semester_info"
