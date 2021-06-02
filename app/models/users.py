import peewee as pw
from app.models.base import get_mysql_model

MySQLModel = get_mysql_model()


class User(MySQLModel):
    email = pw.CharField(max_length=256, unique=True)
    name = pw.CharField(max_length=128)
    self_introduction = pw.CharField(max_length=256)
    phone_number = pw.CharField(max_length=128)
    profile_url = pw.CharField(max_length=256)
    is_active = pw.BooleanField(default=False)


class LocalAuthentication(MySQLModel):
    user = pw.ForeignKeyField(User, backref="local_authentication_info")
    password = pw.CharField(max_length=256)


class SocialAuthentication(MySQLModel):
    user = pw.ForeignKeyField(User, backref="provider_authentication_info")
    platform = pw.CharField(max_length=30)
    sns_service_id = pw.CharField(max_length=100, unique=True)
