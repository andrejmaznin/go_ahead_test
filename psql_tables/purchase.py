import uuid

import sqlalchemy
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import UUID


def create_table(metadata: MetaData) -> Table:
    product = Table(
        'purchase',
        metadata,
        sqlalchemy.Column('id', UUID, default=uuid.uuid4(), primary_key=True),
        sqlalchemy.Column('action_id', UUID, sqlalchemy.ForeignKey('action.id', ondelete='CASCADE'), nullable=False),
        sqlalchemy.Column('type', sqlalchemy.String, nullable=False),
        sqlalchemy.Column('quantity', sqlalchemy.Integer, nullable=False),
    )
    return product
