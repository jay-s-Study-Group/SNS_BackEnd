import peewee as pw
from .base import get_mysql_model

MySQLModel = get_mysql_model()


class User(MySQLModel):
    email = pw.CharField(max_length=256, unique=True)
    password = pw.CharField(max_length=256)
    is_active = pw.BooleanField(default=False)
