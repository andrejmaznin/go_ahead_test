from pydantic import Field, BaseSettings


class PostgreSQLSettings(BaseSettings):
    HOST: str = Field(None, env='PSQL_HOST')
    PORT: int = Field(None, env='PSQL_PORT')
    USER: str = Field(None, env='PSQL_USER')
    PASSWORD: str = Field(None, env='PSQL_PASSWORD')
    DB: str = Field(None, env='PSQL_DB')
    ENV: str = Field(None, env='ENV')
    HEROKU_DATABASE_URL: str = Field(None, env='DATABASE_URL')

    def construct_connection_url(self, driver: str = 'postgresql'):
        if self.ENV == 'test-heroku':
            return f'{driver}{self.HEROKU_DATABASE_URL.lstrip("postgres")}'

        return f'{driver}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'
