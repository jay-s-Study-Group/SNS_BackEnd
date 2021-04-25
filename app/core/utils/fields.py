import peewee as pw
import json


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
