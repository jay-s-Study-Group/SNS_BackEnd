import peewee as pw
from app.databases.session import db


class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db.session


def get_base_model():
    """
    get BaseModel for inheriting other models
    it could return MySQLModel, PostgreSQLModel, etc.
    :rtype: peewee.ModelBase
    """
    return MySQLModel
