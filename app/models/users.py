import peewee as pw
from .base import get_mysql_model

MySQLModel = get_mysql_model()


class User(MySQLModel):
    email = pw.CharField(max_length=256, unique=True)
    password = pw.CharField(max_length=256)
    is_active = pw.BooleanField(default=False)


class SocialAuth(MySQLModel):
    user = pw.ForeignKeyField(User, backref="social_auth_info")
    platform = pw.CharField(max_length=30)
    sns_service_id = pw.CharField(max_length=100, unique=True)
