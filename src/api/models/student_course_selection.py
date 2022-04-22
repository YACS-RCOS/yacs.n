from tortoise import fields
from tortoise.models import Model

class StudentCourseSelection(Model):

    user_id = fields.ForeignKeyField('user_account.user_id')
    semester = fields.TextField()
    course_name = fields.TextField()
    crn = fields.TextField()


    class Meta:
        table = "student_course_selection"
        unique_together = (("user_id", "semester", "course_name", "crn" ),)

