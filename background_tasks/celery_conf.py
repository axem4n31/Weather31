from datetime import timedelta

from celery import Celery
from settings import BROKER_URL

app_celery = Celery(
    'background_tasks',
    backend=BROKER_URL,
    broker=BROKER_URL,
    include=['background_tasks.tasks'],
)

app_celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=1,
    result_expires=3600,
)

app_celery.conf.beat_schedule = {
    'run-test-every-day': {
        'task': 'background_tasks.tasks.recurring_task_once_a_day',
        'schedule': timedelta(minutes=1),
    },
}