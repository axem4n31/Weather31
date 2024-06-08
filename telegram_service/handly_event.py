from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK
from fastapi import Request, HTTPException, Depends

import settings
from models.model_settings import db_helper
from telegram_service.events import start_event, help_event

events_with_db = {
    "/start": start_event,
    "Текущая погода 🌡️": start_event
}
events_without_db = {
    "/help": help_event,
    "Помощь 🆘": help_event
}


async def handle_bot_events(request: Request, secret_key: str, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    check_secret_key(secret_key=secret_key)
    check_method(request=request)
    message = await request.json()
    print(message)
    if 'message' in message:
        if message['message']['text'] in events_with_db:
            await events_with_db[message['message']['text']](message, db=db)
        if message['message']['text'] in events_without_db:
            await events_without_db[message['message']['text']](message)
    return HTTP_200_OK



def check_secret_key(secret_key: str):
    """Функция проверяет серкетный ключ от TELEGRAM WEBHOOK."""
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


def check_method(request: Request):
    """Функция проверяет тип запроса 'POST'"""
    if request.method != 'POST':
        raise HTTPException(status_code=404, detail="Not found")
