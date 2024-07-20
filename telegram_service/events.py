from datetime import time

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import telegram_service.utils
from models.model_services import create_or_update_user, create_or_update_notification
from models.model_settings import db_helper
from models.schemas import CoordinatesSchema, NotificationSchema
from telegram_service.service import send_message, check_user_location, get_user_coordinates, delete_message, \
    check_time_validation
from telegram_service.utils import markup_keyboard, get_location_keyboard, UpdateMessage
from app.weather_services import get_weather, get_city_coordinates, get_weather_by_hours, get_utc_time


async def start_event(chat_id: int, user_tg_id: int, db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """The event is triggered by the command /start and starts the bot."""

    if await check_user_location(user_tg_id=user_tg_id, db=db) is False:
        return await send_message(chat_id=chat_id, text=telegram_service.utils.location_text,
                                  reply_markup=get_location_keyboard)
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
    user_tg_id = int(message['callback_query']['from']['id'])
    chat_id = int(message['callback_query']['message']['chat']['id'])
    lat, lon = await get_user_coordinates(user_tg_id=user_tg_id, db=db)
    weather_by_hours_list = await get_weather_by_hours(lat=lat, lon=lon, days=int(message['callback_query']['data']))

    # Проходимся по каждому прогнозу дня в списке прогнозов

    for weather_by_hours in weather_by_hours_list:
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


async def forecast_event(chat_id: int, user_tg_id: int,
                         db: AsyncSession = Depends(db_helper.scoped_session_dependency)):

    if await check_user_location(user_tg_id=user_tg_id, db=db) is False:
        return await send_message(chat_id=chat_id, text=telegram_service.utils.location_text,
                                  reply_markup=get_location_keyboard)
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
    city_name = message.message.text
    chat_id = message.message.chat.id
    user_tg_id = message.message.from_.id

    # Получаем координаты города
    coordinates_data = await get_city_coordinates(city_name=city_name)

    if coordinates_data is None:
        # Если координаты не найдены, отправляем сообщение о неудаче и возвращаемся
        await send_message(chat_id=chat_id, text=telegram_service.utils.not_found_city_text,
                           reply_markup=markup_keyboard)
        return
    # Создаем пользователя в базе данных

    user_created = await create_or_update_user(
        user_tg_id=user_tg_id,
        coordinates_data=coordinates_data,
        db=db
    )
    # Отправляем соответствующее сообщение в зависимости от результата создания пользователя
    if user_created:
        await send_message(chat_id=chat_id, text='Ваши данные успешно добавлены', reply_markup=markup_keyboard)
    else:
        await send_message(chat_id=chat_id, text='Город успешно изменён', reply_markup=markup_keyboard)


async def help_event(chat_id: int) -> None:
    await send_message(chat_id=chat_id, text=telegram_service.utils.help_text, reply_markup=markup_keyboard)


async def change_region_event(chat_id: int):
    return await send_message(chat_id=chat_id, text=telegram_service.utils.location_text,
                              reply_markup=get_location_keyboard)


async def get_coordinates_from_user_event(message: dict,
                                          db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user_tg_id = int(message['message']['from']['id'])
    chat_id = int(message['message']['chat']['id'])
    message_id = int(message['message']['message_id'])
    await delete_message(chat_id=chat_id, message_id=message_id)
    lat = message['message']['location']['latitude']
    lon = message['message']['location']['longitude']
    if await create_or_update_user(coordinates_data=CoordinatesSchema(lat=lat, lon=lon),
                                   user_tg_id=user_tg_id, db=db) is not True:
        await send_message(chat_id=chat_id, text='Город успешно изменён', reply_markup=markup_keyboard)
        return
    return await send_message(chat_id=chat_id, text='Ваши данные успешно добавлены', reply_markup=markup_keyboard)


async def notification_event(chat_id: int, user_tg_id: int,
                             db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        print(user_tg_id)
        await send_message(chat_id=chat_id, text='Скоро будет', reply_markup=None)
    except Exception as e:
        print(f"Error notification_event : {e}")


async def change_notification_times_event(chat_id: int, user_tg_id: int, time_str: str, db: AsyncSession):
    times = await check_time_validation(chat_id=chat_id, time_str=time_str)
    if times is None:
        return
    notification_data = NotificationSchema(
        chat_id=chat_id,
        time=times,
    )
    result = await create_or_update_notification(user_tg_id=user_tg_id, notification_data=notification_data, db=db)
    text = "Данные успешно сохранены"
    if result is False:
        text = "Необходимо сначала ввести город"
    await send_message(chat_id=chat_id, text=text, reply_markup=markup_keyboard)


