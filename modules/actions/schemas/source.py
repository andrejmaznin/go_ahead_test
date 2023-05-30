import uuid
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import delete, select, exists

from libs.postgresql import get_database
from libs.postgresql.mixin import PostgreSQLMixin
from libs.postgresql.utils import postgresql_settings
from modules.actions.consts import ProductType, ActionType
from modules.actions.schemas.request import ActionRequestSchema
from psql_tables import purchase as purchase_table, action as action_table


@postgresql_settings(table=purchase_table)
class PurchaseSchema(PostgreSQLMixin):
    id: Optional[UUID] = None
    action_id: UUID
    type: ProductType
    quantity: int

    @classmethod
    async def delete_for_action(cls, action_id: UUID):
        await get_database().execute(
            query=delete(cls.psql_table).where(cls.psql_table.action_id == action_id)
        )

    @classmethod
    def from_request(cls, action_schema: ActionRequestSchema) -> List['PurchaseSchema']:
        products_quantity = {}
        for product in action_schema.products:
            products_quantity[product.type] = products_quantity.get(product.type, 0) + 1
        return [
            cls(
                id=uuid.uuid4(),
                action_id=action_schema.id,
                type=p_t,
                quantity=q
            ) for p_t, q in products_quantity.items()
        ]


@postgresql_settings(table=action_table)
class ActionSchema(PostgreSQLMixin):
    id: Optional[UUID] = None
    datetime: datetime
    user_id: int
    site_id: int
    action: ActionType
    page_id: Optional[int] = None

    @classmethod
    async def check_exists(cls, id_: UUID) -> bool:
        query = select(exists().where(cls.psql_table.c.id == id_))
        result = await get_database().execute(query=query)
        return result