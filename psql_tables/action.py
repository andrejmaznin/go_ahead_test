import sqlalchemy
from sqlalchemy import MetaData, Table, text
from sqlalchemy.dialects.postgresql import UUID


def create_table(metadata: MetaData) -> Table:
    action = Table(
        'action',
        metadata,
        sqlalchemy.Column('id', UUID(as_uuid=True), server_default=text('gen_random_uuid()'), primary_key=True),
        sqlalchemy.Column('datetime', sqlalchemy.TIMESTAMP, nullable=False),
        sqlalchemy.Column('user_id', sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column('site_id', sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column('action', sqlalchemy.Text, nullable=False),
        sqlalchemy.Column('page_id', sqlalchemy.Integer, nullable=True)
    )
    return action
