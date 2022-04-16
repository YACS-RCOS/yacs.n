import tortoise
from tortoise.contrib.postgres import fields as pfields
from tortoise import fields
from tortoise.models import Model


class Course(Model):
    crn = fields.CharField(max_length=255, pk=True)
    section = fields.CharField(max_length=255, null=True)
    semester = fields.CharField(max_length=255, null=True)
    min_credits = fields.IntField(null=True)
    max_credits = fields.IntField(null=True)
    date_start = fields.DateField(null=True)
    date_end = fields.DateField(null=True)
    department = fields.CharField(max_length=255, null=True)
    level = fields.IntField(null=True)
    title = fields.CharField(max_length=255, null=True)
    full_title = fields.TextField(null=True)
    description = fields.TextField(null=True)
    raw_precoreqs = fields.TextField(null=True)
    frequency = fields.CharField(max_length=255, null=True)
    school = fields.CharField(max_length=255, null=True)
    seats_open = fields.IntField(null=True)
    seats_filled = fields.IntField(null=True)
    seats_total = fields.IntField(null=True)
    tsv = pfields.TSVectorField(null=True)

    class Meta:
        table = "course"