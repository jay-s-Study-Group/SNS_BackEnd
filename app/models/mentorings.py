import peewee as pw
from app.models.base import get_mysql_model

MySQLModel = get_mysql_model()


class MentorApplication(MySQLModel):
    id = pw.BooleanField()
    confirm_flag = pw.BooleanField()
    mentoringfield = pw.IntegerField()
    user_id = pw.IntegerField()
    application_date = pw.DateTimeField()
    approver_name = pw.CharField(255)
    price = pw.IntegerField()
    capacity = pw.IntegerField()
    approve_date = pw.DateTimeField()
    mentoring_name = pw.CharField(max_length=255)
    mentoring_description = pw.TextField()

class ClassRoom(MySQLModel):
    id = pw.IntegerField()
    mentoring_id = pw.IntegerField()
    classroom_type = pw.IntegerField()
    content = pw.TextField()
    content_file = pw.CharField(max_length=150)

class ClassRoomType(MySQLModel):
    id = pw.IntegerField()
    type_name = pw.CharField(max_length=255)
    description = pw.TextField()