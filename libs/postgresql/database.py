from databases import Database
from dotenv import load_dotenv

from ..postgresql.settings import PostgreSQLSettings

load_dotenv()
psql_settings = PostgreSQLSettings()

database = None


def get_database():
    global database
    if database is None:
        database = Database(
            url=psql_settings.construct_connection_url(driver='postgresql+asyncpg')
        )
    return database
