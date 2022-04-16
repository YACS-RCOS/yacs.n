from tortoise import fields
from tortoise.models import Model

class CoursePrerequisite(Model):
    department = fields.CharField(max_length=255)
    level = fields.IntField()
    prerequisite = fields.CharField(max_length=255)
    
    class Meta:
        table = "course_prerequisite"
        unique_together = (("department", "level", "prerequisite"),)
