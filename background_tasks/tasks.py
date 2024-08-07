import asyncio
import json
import requests
import nest_asyncio
from sqlalchemy import select, or_
from celery import Celery
from datetime import timedelta
from app.weather_services import get_utc_time, get_weather
from models.model import User
from models.model_settings import async_session
from background_tasks.celery_conf import app_celery
from settings import BASE_HOST, TOKEN_WEATHER_31
from telegram_service.service import send_message, validation_str_to_time

nest_asyncio.apply()


@app_celery.task
def recurring_task_once_a_day():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_time_task())
    except Exception as e:
        print(f"Error : {e}")


async def create_time_task():
    async with async_session() as session:
        result = await session.execute(
            select(User).where(or_(User.notifications_json.isnot(None)))
        )
        users = result.scalars().all()
        if users:
            for user in users:
                lat, lon = user.lat, user.lon
                notifications = json.loads(user.notifications_json)
                chat_id = notifications["chat_id"]
                times_str = notifications["time"]
                times_obj = await validation_str_to_time(time_list_str=times_str)
                eta_time = await get_utc_time(lat=lat, lon=lon, times=times_obj)
                for i in eta_time:
                    print(i)
                    send_message_task.apply_async(args=[chat_id, lat, lon])


@app_celery.task
def send_message_task(chat_id: int, lat: float, lon: float):
    # current_weather = await get_weather(lat=lat, lon=lon, days=1)
    # more_details_by_hour = {
    #     "inline_keyboard": [
    #         [{"text": "Подробней по часам", "callback_data": current_weather.days[0].is_day}]],
    # }
    # text = f"{current_weather.text}, {current_weather.temp}°C ощущается как {current_weather.feels_like}°C." \
    #        f"\nОблачность {current_weather.cloud}%. Влажность {current_weather.humidity}%." \
    #        f"\n{current_weather.city}, {current_weather.region}, {current_weather.country}"
    # await send_message(chat_id=chat_id, text=text, reply_markup=more_details_by_hour)
    try:
        url_weather = BASE_HOST + 'api/find_out_the_weather'
        print(url_weather)
        data = {
            "city": [{
                "lat": lat,
                "lon": lon,
            }],
            "days": 1,
            "token": TOKEN_WEATHER_31
        }
        weather = requests.post(url_weather, data=data)
        print(weather)
    except Exception as e:
        print(f"Error send_message_task : {e}")


