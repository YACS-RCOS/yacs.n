from tortoise import fields
from tortoise.models import Model
from tortoise.contrip.postgres.fields import TSVectorField


class Course(Model):
    __tablename__ = "course"

    crn = fields.CharField(max_length=255, primary_key=True)
    section = fields.CharField(max_length=255)
    semester = fields.CharField(max_length=255)
    min_credits = fields.IntField()
    max_credits = fields.IntField()
    date_start = fields.DatetimeField()
    date_end = fields.DatetimeField()
    department = fields.CharField(max_length=255)
    level = fields.IntField()
    title = fields.CharField(max_length=255)
    full_title = fields.TextField()
    description = fields.TextField()
    raw_precoreqs = fields.TextField()
    frequency = fields.CharField(max_length=255)
    school = fields.CharField(max_length=255)
    seats_open = fields.IntField()
    seats_filled = fields.IntField()
    seats_total = fields.IntField()
    tsv = TSVectorField()

    class Meta:
        table = "course"