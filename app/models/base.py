import peewee as pw
from app.core.databases import db


class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db.session


def get_mysql_model():
    """
    get BaseModel for inheriting other models
    it could return MySQLModel
    :rtype: peewee.ModelBase
    """
    return MySQLModel
