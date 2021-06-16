import peewee as pw
from app.models.base import get_mysql_model

MySQLModel = get_mysql_model()


class MentorApplication(MySQLModel):
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
