from celery import Celery
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_settings import db_helper
from settings import BROKER_URL

app_celery = Celery(
    'tasks',
    backend=BROKER_URL,
    broker=BROKER_URL
)

app_celery.conf.update(
    task_serializer='json',
    result_serializer='json',
)


async def send_notification(db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    pass
