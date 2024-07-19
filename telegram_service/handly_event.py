
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK
from fastapi import Request, HTTPException, Depends
import settings
from models.model_settings import db_helper
from telegram_service.events import start_event, help_event, registration_event, change_region_event, forecast_event, \
    get_coordinates_from_user_event, by_hourly_event, notification_event

events_with_db = {
    "/notifications": notification_event,
    "Уведомления 🔔": notification_event,
    "/start": start_event,
    "Текущая погода 🌡️": start_event,
    "/forecast": forecast_event,
    "Прогноз погоды 🌤️": forecast_event,
}
events_without_db = {
    "/help": help_event,
    "Помощь 🆘": help_event,
    "/change_region": change_region_event,
    "Изменить регион 🌍": change_region_event,
}

# todo можно добавить проверку типа сообщений


async def handle_bot_events(request: Request, secret_key: str,
                            db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """
    The function checks the user's response and triggers the corresponding event
    """
    # Проверка секретного ключа и метода запроса
    check_secret_key(secret_key=secret_key)
    check_method(request=request)

    try:
        # Получение данных из запроса
        message = await request.json()
        print(message)
        if 'message' in message:
            # Если в сообщении есть текст, обрабатываем его
            if 'text' in message['message']:
                text = message['message']['text']
                chat_id = int(message['message']['chat']['id'])
                user_tg_id = int(message['message']['from']['id'])
                if text in events_with_db:
                    await events_with_db[text](chat_id, user_tg_id, db=db)
                elif text in events_without_db:
                    await events_without_db[text](chat_id)
                else:
                    await registration_event(message=message, db=db)

            # Если в сообщении есть местоположение, вызываем соответствующую функцию
            elif 'location' in message['message']:
                await get_coordinates_from_user_event(message, db=db)

        elif 'callback_query' in message and 'data' in message['callback_query']:
            # Если в запросе есть callback_query с данными, вызываем by_hourly_event
            await by_hourly_event(message, db=db)

        return HTTP_200_OK
    except Exception as e:
        print(f"Error handle_bot_events : {e}")


def check_secret_key(secret_key: str):
    """Функция проверяет серкетный ключ от TELEGRAM WEBHOOK."""
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


def check_method(request: Request):
    """Функция проверяет тип запроса 'POST'"""
    if request.method != 'POST':
        raise HTTPException(status_code=404, detail="Not found")
