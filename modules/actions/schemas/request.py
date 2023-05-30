from typing import List, Optional
from uuid import UUID

import datetime as datetime
from pydantic import BaseModel, root_validator, Field
from datetime import datetime
from modules.actions.consts import ActionType, ProductType, MetricType


class PurchaseRequestSchema(BaseModel):
    type: ProductType


class ActionRequestSchema(BaseModel):
    id: UUID
    datetime: datetime
    user_id: int
    site_id: int
    action: ActionType
    products: List[PurchaseRequestSchema] = []
    page_id: Optional[int] = None

    @root_validator
    def check_correct_action_type(cls, values):
        if values.get('action') == ActionType.PURCHASE and \
            not all([values.get('products'), values.get('page_id') is None]):
            raise ValueError('wrong schema format')
        if values.get('action') == ActionType.VISIT and any([values.get('products'), values.get('page_id') is None]):
            raise ValueError('wrong schema format')
        return values


class FilterSchema(BaseModel):
    from_number: int = Field(..., alias='from')
    to_number: int = Field(0, alias='to')
    metric: MetricType
    products: Optional[ProductType] = None


class SiteSearchRequestSchema(BaseModel):
    from_date: datetime = Field(..., alias='from')
    to_date: datetime = Field(..., alias='to')
    filters: List[FilterSchema] = []
