from fastapi import APIRouter

from modules.actions.internals import get_site_ids_for_filters
from modules.actions.schemas.request import SiteSearchRequestSchema
from modules.actions.schemas.response import SiteSearchResponseSchema

router = APIRouter()


@router.post(path='/search', status_code=200)
async def search_sites(request: SiteSearchRequestSchema):
    site_ids = await get_site_ids_for_filters(start=request.from_date, end=request.to_date, filters=request.filters)
    return SiteSearchResponseSchema(site_ids=site_ids)
