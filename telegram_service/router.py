from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from models.model_settings import db_helper
from telegram_service.handly_event import handle_bot_events

event_router = APIRouter(prefix="/handle_bot_events", tags=["Handle events"])


@event_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str,
                                   db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await handle_bot_events(request=request, secret_key=secret_key, db=db)
