from fastapi import APIRouter, HTTPException

from libs.postgresql import get_database
from modules.actions.schemas.request import ActionRequestSchema
from modules.actions.schemas.source import ActionSchema, PurchaseSchema

router = APIRouter()


@router.post(path='/add', status_code=200)
async def add_action(action: ActionRequestSchema):
    if await ActionSchema.check_exists(action.id):
        raise HTTPException(status_code=400, detail=f'Action with id {action.id} already exists')

    new_action = ActionSchema(
        id=action.id,
        datetime=action.datetime,
        user_id=action.user_id,
        site_id=action.site_id,
        action=action.action
    )
    # will be empty if action is visit
    new_purchases = PurchaseSchema.from_request(action_schema=action)

    connection = get_database().connection()
    async with connection.transaction():
        await new_action.insert()
        await PurchaseSchema.bulk_insert(new_purchases)


@router.post(path='/edit', status_code=200)
async def edit_action(action: ActionRequestSchema):
    if not await ActionSchema.check_exists(action.id):
        raise HTTPException(status_code=400, detail=f'Action with id {action.id} does not exist')

    # if action changed from purchase to visit, will clear products
    # if action remained visit, will do nothing
    # if action remained purchase, will replace with products from request
    await PurchaseSchema.delete_for_action(action_id=action.id)

    action_to_edit = ActionSchema(
        id=action.id,
        datetime=action.datetime,
        user_id=action.user_id,
        site_id=action.site_id,
        action=action.action
    )
    # will be empty if action is visit
    replaced_purchases = PurchaseSchema.from_request(action_schema=action)

    connection = get_database().connection()
    async with connection.transaction():
        await action_to_edit.insert()
        await PurchaseSchema.bulk_insert(replaced_purchases)
