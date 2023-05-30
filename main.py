import logging

from fastapi import FastAPI

from libs.postgresql import get_database
from modules.actions.routes import actions_router, sites_router

logger = logging.getLogger(__name__)

logger.info('Creating FastAPI app...')
app = FastAPI(title='Go Ahead Test Task')
app.include_router(router=actions_router, prefix='/actions')
app.include_router(router=sites_router, prefix='/sites')


@app.on_event(event_type='startup')
async def startup():
    database = get_database()
    await database.connect()


@app.on_event(event_type='shutdown')
async def shutdown():
    database = get_database()
    await database.disconnect()
