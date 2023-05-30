from typing import List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from .database import get_database


class PostgreSQLMixin(BaseModel):
    async def insert(self):
        async with get_database().connection() as connection:
            async with connection.transaction():
                result = await connection.execute(
                    query=insert(self.psql_table).on_conflict_do_update(
                        constraint=self.psql_table.primary_key,
                        set_=self.dict(exclude={'id'})
                    ).returning(self.psql_table),
                    values=self.dict()
                )
        return result

    @classmethod
    async def bulk_insert(cls, objects: List['PostgreSQLMixin']):
        async with get_database().connection() as connection:
            async with connection.transaction():
                await connection.execute_many(
                    query=insert(cls.psql_table),
                    values=[obj.dict() for obj in objects]
                )

    @classmethod
    async def get_by_id(cls, id: UUID):
        async with get_database().connection() as connection:
            query = cls.psql_table.select().where(cls.psql_table.c.id == id)
            row = await connection().fetch_one(query)
            print(row)
        return cls(**row)
