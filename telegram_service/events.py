from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import httpx

import settings
from models.model_services import create_user
from models.model_settings import db_helper
from models.schemas import CoordinatesSchema
from telegram_service.service import send_message, check_user_location, get_user_coordinates, delete_message
from telegram_service.utils import markup_keyboard, get_location_keyboard, UpdateMessage
from weather_services import get_weather, get_city_coordinates, get_weather_by_hours

client = httpx.AsyncClient()


async def start_event(message: UpdateMessage.dict, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """Ивент вызывается командой /start и начинает работу бота"""

    message = UpdateMessage.parse_obj(message)
    # chat_id = int(message['message']['chat']['id'])
    # user_tg_id = int(message['message']['from']['id'])
    chat_id = message.message.chat.id
    user_tg_id = message.message.from_.id
    if await check_user_location(user_tg_id=user_tg_id, db=db) is False:
        return await send_message(chat_id=chat_id, text=settings.location_text, reply_markup=get_location_keyboard)
    lat, lon = await get_user_coordinates(user_tg_id=user_tg_id, db=db)
    current_weather = await get_weather(lat=lat, lon=lon, days=1)
    more_details_by_hour = {
        "inline_keyboard": [
            [{"text": "Подробней по часам", "callback_data": current_weather.days[0].is_day}]],
    }
    text = f"{current_weather.text}, {current_weather.temp}°C ощущается как {current_weather.feels_like}°C." \
           f"\nОблачность {current_weather.cloud}%. Влажность {current_weather.humidity}%." \
           f"\n{current_weather.city}, {current_weather.region}, {current_weather.country}"
    await send_message(chat_id=chat_id, text=text, reply_markup=more_details_by_hour)


async def by_hourly_event(message: dict, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    print('lol')
    user_tg_id = int(message['callback_query']['from']['id'])
    chat_id = int(message['callback_query']['message']['chat']['id'])
    lat, lon = await get_user_coordinates(user_tg_id=user_tg_id, db=db)
    weather_by_hours_list = await get_weather_by_hours(lat=lat, lon=lon, days=int(message['callback_query']['data']))
    print(len(weather_by_hours_list), "ДЛИНААААААААА")
    # Проходимся по каждому прогнозу дня в списке прогнозов
    for weather_by_hours in weather_by_hours_list:
        print(weather_by_hours.text)
        # Проходимся по каждому часу в прогнозе текущего дня
        for hour in weather_by_hours.hours:
            print(hour.time, hour.text, hour.temp, hour.humidity)
            text = f"{hour.time}" \
                   f"\n{hour.text}" \
                   f"\n{hour.temp}°C ощущается как {hour.feels_like}°C" \
                   f"\nСкорость ветра {hour.wind_kph} км/ч" \
                   f"\nВлажность {hour.humidity}%" \
                   f"\nВероятность дождя {hour.chance_of_rain}%"
            await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)


async def forecast_event(message: dict, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    # Извлекаем необходимые данные из сообщения
    chat_id = int(message['message']['chat']['id'])
    user_tg_id = int(message['message']['from']['id'])
    if await check_user_location(user_tg_id=user_tg_id, db=db) is False:
        return await send_message(chat_id=chat_id, text=settings.location_text, reply_markup=get_location_keyboard)
    lat, lon = await get_user_coordinates(user_tg_id=user_tg_id, db=db)
    current_weather = await get_weather(lat=lat, lon=lon, days=7)
    for day in current_weather.days:
        more_details_by_hour = {
            "inline_keyboard": [
                [{"text": "Подробней по часам", "callback_data": day.is_day}]],
        }
        text = f"{day.text}" \
               f"\nМаксимальная температура {day.max_temp}°C" \
               f"\nМинимальная температура {day.min_temp}°C" \
               f"\nВероятность дождя {day.daily_chance_of_rain}%" \
               f"\nМаксимальная скорость ветра {day.max_wind_kph} км/ч" \
               f"\nИндекс ультрофиолета {day.uv}" \
               f"\n{day.date}"
        await send_message(chat_id=chat_id, text=text, reply_markup=more_details_by_hour)


async def registration_event(
        message: UpdateMessage.dict,
        db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """Функция вызывается для добавления"""
    # Извлекаем необходимые данные из сообщения
    message = UpdateMessage.parse_obj(message)
    # city_name = message['message']['text']
    # chat_id = int(message['message']['chat']['id'])
    # user_tg_id = int(message['message']['from']['id'])
    city_name = message.message.text
    chat_id = message.message.chat.id
    user_tg_id = message.message.from_.id

    # Получаем координаты города
    coordinates_data = await get_city_coordinates(city_name=city_name)

    if coordinates_data is None:
        # Если координаты не найдены, отправляем сообщение о неудаче и возвращаемся
        await send_message(chat_id=chat_id, text=settings.not_found_city_text, reply_markup=markup_keyboard)
        return

    # Создаем пользователя в базе данных
    user_created = await create_user(user_tg_id=user_tg_id, coordinates_data=coordinates_data, db=db)

    # Отправляем соответствующее сообщение в зависимости от результата создания пользователя
    if user_created:
        await send_message(chat_id=chat_id, text='Ваши данные успешно добавлены', reply_markup=markup_keyboard)
    else:
        await send_message(chat_id=chat_id, text='Город успешно изменён', reply_markup=markup_keyboard)


async def help_event(message: dict):
    chat_id = int(message['message']['chat']['id'])
    await send_message(chat_id=chat_id, text=settings.help_text, reply_markup=markup_keyboard)


async def change_region_event(message: dict):
    chat_id = int(message['message']['chat']['id'])
    return await send_message(chat_id=chat_id, text=settings.location_text, reply_markup=get_location_keyboard)


async def get_coordinates_from_user_event(message: dict,
                                          db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user_tg_id = int(message['message']['from']['id'])
    chat_id = int(message['message']['chat']['id'])
    message_id = int(message['message']['message_id'])
    await delete_message(chat_id=chat_id, message_id=message_id)
    lat = message['message']['location']['latitude']
    lon = message['message']['location']['longitude']
    if await create_user(user_tg_id=user_tg_id, coordinates_data=CoordinatesSchema(lat=lat, lon=lon), db=db) is True:
        return await send_message(chat_id=chat_id, text='Ваши данные успешно добавлены', reply_markup=markup_keyboard)
    await send_message(chat_id=chat_id, text='Город успешно изменён', reply_markup=markup_keyboard)

