import asyncio
import nest_asyncio
from sqlalchemy import select, or_
from celery import Celery
from datetime import timedelta



from app.weather_services import get_utc_time
from models.model import User
from models.model_settings import async_session
from background_tasks.celery_conf import app_celery

nest_asyncio.apply()


@app_celery.task
def test():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_test())
    except Exception as e:
        print(f"Error : {e}")


async def async_test():
    async with async_session() as session:
        user = await session.scalar(select(User).where(or_(User.notifications_json.isnot(None))))
        if user:
            user_id = user.user_tg_id
            lat, lon = user.lat, user.lon
            print(lat, lon)
            eta_time = await get_utc_time(lat=lat, lon=lon)
            eta_time += timedelta(seconds=5)
            send_message_task.apply_async(args=[user_id], eta=eta_time)


@app_celery.task
def send_message_task(user_id: int):
    print(user_id)


@app_celery.task
def add(message: dict):
    print(message)
    return message['x'] * message['y']
    # вызов данной функции
    # eta_time = datetime.now() + timedelta(seconds=5) - timedelta(hours=3)
    # print(eta_time)
    # data = {"x": 6, "y": 11}
    # result = add.apply_async(args=[data], eta=eta_time)


