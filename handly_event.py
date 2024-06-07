from starlette.status import HTTP_200_OK
from fastapi import Request, HTTPException

import settings
from events import start_event

events = {
    "/start": start_event,
    "Текущая погода 🌡️": start_event
}


async def handle_bot_events(request: Request, secret_key: str):
    check_secret_key(secret_key=secret_key)
    check_method(request=request)
    message = await request.json()
    print(message)
    if 'message' in message:
        if message['message']['text'] in events:
            await events[message['message']['text']](message)
    return HTTP_200_OK



def check_secret_key(secret_key: str):
    """Функция проверяет серкетный ключ от TELEGRAM WEBHOOK."""
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


def check_method(request: Request):
    """Функция проверяет тип запроса 'POST'"""
    if request.method != 'POST':
        raise HTTPException(status_code=404, detail="Not found")
