from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import settings
import httpx

from models.model_settings import db_helper
from telegram_service.service import send_message, check_user_location, get_user_coordinates
from telegram_service.utils import markup_keyboard, markup_inline_get_location
from weather_services import get_current_weather

client = httpx.AsyncClient()


async def start_event(message, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    chat_id = int(message['message']['chat']['id'])
    user_tg_id = int(message['message']['from']['id'])
    if await check_user_location(user_tg_id=user_tg_id, db=db) is False:
        text = "Для получения информации о погоде, пожалуйста, укажите название города (напишите его в чат) или поделитесь геолокацией"
        return await send_message(chat_id=chat_id, text=text, reply_markup=markup_inline_get_location)
    lat, lon = await get_user_coordinates(user_tg_id=user_tg_id, db=db)
    current_weather = await get_current_weather(lat=lat, lon=lon)
    # временный словари
    text = f"{current_weather.temp}°C ощущается как {current_weather.feels_like}°C, Облачность {current_weather.cloud}%"
    await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)


async def help_event(message):
    chat_id = int(message['message']['chat']['id'])
    text = "Хэлпа мужика, хэлпа"
    await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)