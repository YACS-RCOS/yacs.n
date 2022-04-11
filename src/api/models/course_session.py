from tortoise import fields
from tortoise.models import Model


class CourseSession(Model):
    crn = fields.CharField(max_length=255)
    section = fields.CharField(max_length=255)
    semester = fields.CharField(max_length=255)
    time_start = fields.TimeField()
    time_end = fields.TimeField()
    day_of_week = fields.IntField()
    location = fields.CharField(max_length=255)
    session_type = fields.CharField(max_length=255)
    instructor = fields.CharField(max_length=255)

    class Meta:
        table = "course_session"
        unique_together = (('crn', 'section', 'semester', 'day_of_week'),)