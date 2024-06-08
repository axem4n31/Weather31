from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import settings
import httpx

from models.model_services import create_user
from models.model_settings import db_helper
from telegram_service.service import send_message, check_user_location, get_user_coordinates
from telegram_service.utils import markup_keyboard, markup_inline_get_location
from weather_services import get_current_weather, get_city_coordinates

client = httpx.AsyncClient()


async def start_event(message: dict, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
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


async def registration_event(message: dict, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    coordinates_data = await get_city_coordinates(city_name=message['message']['text'])
    chat_id = int(message['message']['chat']['id'])
    user_tg_id = int(message['message']['from']['id'])
    text = 'Город не найден, введите корректное название'
    if coordinates_data is None:
        return await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)

    text = 'Для изменения региона воспользуйтесь командой /settings'
    if await create_user(user_tg_id=user_tg_id, coordinates_data=coordinates_data, db=db) is False:
        return await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)
    await send_message(chat_id=chat_id, text='Ваши данные успешно добавлены!', reply_markup=markup_keyboard)


async def help_event(message: dict):
    chat_id = int(message['message']['chat']['id'])
    text = "Хэлпа мужика, хэлпа"
    await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)