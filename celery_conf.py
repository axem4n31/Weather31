from celery import Celery
from settings import BROKER_URL
# Инициализация приложения Celery
app_celery = Celery(
    'tasks',
    backend=BROKER_URL,
    broker=BROKER_URL,
    include=['tasks']
)

app_celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=1,  # Опционально: количество одновременно выполняющихся задач
)
