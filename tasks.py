import asyncio
from datetime import timedelta

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


@app_celery.task()
def test():
    print("Тест")


@app_celery.task
def add(message: dict):
    try:
        result = asyncio.run(help_event(message))
    except Exception as ex:
        raise


app_celery.conf.beat_schedule = {
    'run-test-every-day': {
        'task': 'tasks.test',
        'schedule': timedelta(minutes=10),
    },
}

