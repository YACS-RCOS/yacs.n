from tortoise import fields
from tortoise.models import Model


class CourseSession(Model):
    crn = fields.VarcharField(max_length=255)
    section = fields.VarcharField(max_length=255)
    semester = fields.VarcharField(max_length=255)
    time_start = fields.TimeField()
    time_end = fields.TimeField()
    day_of_week = fields.IntegerField()
    location = fields.VarcharField(max_length=255)
    session_type = fields.VarcharField(max_length=255)
    instructor = fields.VarcharField(max_length=255)

    class Meta:
        table = "course_session"
        unique_together = (('crn', 'section', 'semester', 'day_of_week'),)