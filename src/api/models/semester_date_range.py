from unittest.util import _MAX_LENGTH
from tortoise import fields
from tortoise.models import Model


class SemesterDateRange(Model):
    semester_part_name = fields.CharField(max_length = 255, null = True)
    date_start = fields.DateField()
    date_end = fields.DateField()


    class Meta:
        table = 'semester_date_range'
        unique_together = (('date_start', 'date_end'),)
