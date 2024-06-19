from datetime import datetime
from celery import Celery
from celery.utils.log import get_task_logger
from settings import BROKER_URL
from telegram_service.events import help_event

logger = get_task_logger(__name__)

app_celery = Celery(
    'tasks',
    backend=BROKER_URL,
    broker=BROKER_URL
)

app_celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@app_celery.task
async def add(x, y):

    data = {
        "x": x,
        "y": y,
        "z": x * y
    }
    current_time = datetime.now()
    print(f"Время выполнения: {current_time}")

    return data


