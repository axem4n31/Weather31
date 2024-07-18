import asyncio
import nest_asyncio
from sqlalchemy import select
from celery import Celery
from datetime import timedelta
from models.model import User
from models.model_settings import async_session
from background_tasks.celery_conf import app_celery

nest_asyncio.apply()


@app_celery.task
def test(x):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_test(x))
    except Exception as e:
        print(f"Error : {e}")


async def async_test(x: int):
    async with async_session() as session:
        print("123" * x)
        id_tg = 886953788
        user = await session.scalar(select(User).where(User.notifications_json is not None))
        print(user.user_tg_id)


@app_celery.task
def add(message: dict):
    print(message)
    return message['x'] * message['y']
    # вызов данной функции
    # eta_time = datetime.now() + timedelta(seconds=5) - timedelta(hours=3)
    # print(eta_time)
    # data = {"x": 6, "y": 11}
    # result = add.apply_async(args=[data], eta=eta_time)


