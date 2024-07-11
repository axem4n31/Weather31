import asyncio
from datetime import timedelta
from celery.utils.log import get_task_logger
from celery_conf import app_celery
from settings import BROKER_URL
from telegram_service.events import help_event

# Определение логгера для асинхронных задач
logger = get_task_logger(__name__)


@app_celery.task()
async def test():
    logger.info("Тест")
    print("Тест")


@app_celery.task(bind=True)
async def add(self, message: dict):
    logger.info(f"Задача add получила сообщение: {message}")
    print(message)
    try:
        result = await help_event(message)
        logger.info(f"Результат обработки сообщения: {result}")
    except Exception as e:
        error_msg = f"Ошибка при обработке сообщения: {e}"
        print(error_msg)
        logger.error(error_msg)

app_celery.conf.beat_schedule = {
    'run-test-every-day': {
        'task': 'tasks.test',
        'schedule': timedelta(minutes=10),
    },
}