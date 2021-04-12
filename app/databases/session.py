import peewee as pw
from app.common.util import conf
import functools


class PeeweeDBConnection:
    def __init__(self):
        self._session = pw.MySQLDatabase(
            database=conf().DATABASE_NAME,
            host=conf().DATABASE_HOST,
            port=conf().DATABASE_PORT,
            user=conf().DATABASE_USER,
            passwd=conf().DATABASE_PASSWD,
        )

    @property
    def session(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._session.is_closed():
            self._session.close()

    def db_connect(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self._session.connection_context():
                return func(*args, **kwargs)

        return wrapper

    def create_tables(self, tables):
        uncreated_tables = [
            table for table in tables if not self._session.table_exists(table)
        ]
        self._session.create_tables(uncreated_tables)


db = PeeweeDBConnection()
