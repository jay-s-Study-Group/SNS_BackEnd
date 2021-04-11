import peewee as pw
import json
from app.common.util import conf

conn = pw.MySQLDatabase(
    "",
    host=conf().DATABASE_HOST,
    port=conf().DATABASE_PORT,
    user=conf().DATABASE_USER,
    passwd=conf().DATABASE_PASSWD,
)


class JSONField(pw.TextField):
    def __init__(self):
        super(JSONField, self).__init__()
        self.isContain = False

    def db_value(self, value):
        if self.isContain:
            output = super().db_value(value)
            self.isContain = False
            return output
        return json.dumps(value, ensure_ascii=False)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

    def contains(self, value):
        value = "%%%s%%" % value
        self.isContain = True
        return pw.Expression(self, pw.OP.ILIKE, value)


class MySQLModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = skyhub
