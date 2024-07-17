import asyncio
from datetime import timedelta
from celery.utils.log import get_task_logger
from background_tasks.celery_conf import app_celery
from telegram_service.events import help_event

# Определение логгера для асинхронных задач
logger = get_task_logger(__name__)


@app_celery.task()
async def test():
    logger.info("Тест")
    print("Тест")


@app_celery.task
def add(message: dict):
    print(message)
    return message['x'] * message['y']
    # вызов данной функции
    # eta_time = datetime.now() + timedelta(seconds=5) - timedelta(hours=3)
    # print(eta_time)
    # data = {"x": 6, "y": 11}
    # result = add.apply_async(args=[data], eta=eta_time)


app_celery.conf.beat_schedule = {
    'run-test-every-day': {
        'task': 'tasks.test',
        'schedule': timedelta(minutes=1),
    },
}