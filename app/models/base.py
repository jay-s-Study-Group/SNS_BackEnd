from typing import Iterable, Iterator
import peewee as pw
import functools
from app.core.databases import db
from typing import Generator


class classproperty(object):
    def __init__(self, function):
        self.function = function

    def __get__(self, owner_self, owner_cls):
        return self.function(owner_cls)


class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db.session

    @classproperty
    def unique_fields(cls) -> Generator[object, None, None]:
        for field_name in cls._meta.fields.keys():
            field = getattr(cls, field_name)
            if field.unique == True or field.primary_key == True:
                yield field


def get_mysql_model():
    """
    get BaseModel for inheriting other models
    it could return MySQLModel
    :rtype: peewee.ModelBase
    """
    return MySQLModel
