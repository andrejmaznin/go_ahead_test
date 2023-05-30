from typing import List

from pydantic import BaseModel


class SiteSearchResponseSchema(BaseModel):
    site_ids: List[int] = []
