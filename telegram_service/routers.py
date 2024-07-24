from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.weather_services import check_token
from models.model_settings import db_helper
from telegram_service.handly_event import handle_bot_events
from telegram_service.service import send_message

event_router = APIRouter(prefix="/handle_bot_events", tags=["Handle events"])
telegram_router = APIRouter(prefix="/telegram", tags=["Telegram"])


@event_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str,
                                   db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await handle_bot_events(request=request, secret_key=secret_key, db=db)


@telegram_router.get('/send_message')
async def send_message_router(chat_id: int, text: str, reply_markup: None | dict, token: str):
    await check_token(token=token)
    await send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
