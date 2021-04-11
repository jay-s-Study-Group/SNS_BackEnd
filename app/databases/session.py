import peewee as pw
from app.common.util import conf

conn = pw.MySQLDatabase(
    "",
    host=conf().DATABASE_HOST,
    port=conf().DATABASE_PORT,
    user=conf().DATABASE_USER,
    passwd=conf().DATABASE_PASSWD,
)
