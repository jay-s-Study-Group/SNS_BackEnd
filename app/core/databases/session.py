import peewee as pw
from core.config import load_config
import functools

CONFIG = load_config()


class PeeweeDBConnection:
    def __init__(self):
        self._session = pw.MySQLDatabase(
            database=CONFIG.DATABASE_NAME,
            host=CONFIG.DATABASE_HOST,
            port=CONFIG.DATABASE_PORT,
            user=CONFIG.DATABASE_USER,
            passwd=CONFIG.DATABASE_PASSWD,
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
