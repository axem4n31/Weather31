import json
from datetime import time
from typing import Tuple, List

from httpx import AsyncClient
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import settings
from models.model import User


async def send_message(chat_id: int, text: str, reply_markup: None | dict) -> None:
    url = settings.TELEGRAM_API_URL + 'sendMessage'
    if reply_markup:
        reply_markup = json.dumps(reply_markup)
    params = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }
    async with AsyncClient() as client:
        await client.post(url, data=params)


async def check_user_location(user_tg_id: int, db: AsyncSession) -> bool:
    user = await db.scalar(select(User).where(and_(User.user_tg_id == user_tg_id)))
    if user:
        return True
    return False


async def get_user_coordinates(user_tg_id: int, db: AsyncSession) -> Tuple[float, float]:
    user = await db.scalar(select(User).where(and_(User.user_tg_id == user_tg_id)))
    lat = user.lat
    lon = user.lon
    return lat, lon


async def delete_message(chat_id: int, message_id: int) -> None:
    url = settings.TELEGRAM_API_URL + 'deleteMessage'
    params = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    async with AsyncClient() as client:
        await client.post(url, data=params)


async def check_time_validation(chat_id: int, time_str: str) -> List[str]:
    array_str_time = []
    time_list_str = time_str.strip('[]').strip()
    if ',' in time_str:
        time_list_str = time_str.strip('[]').split(', ')

    try:
        await validation_str_to_time(time_list_str=time_list_str)
        if isinstance(time_list_str, list):
            return time_list_str
        array_str_time.append(time_list_str)
        return array_str_time

    except Exception as e:
        print(f"Error change_notification_times_event : {e}")
        await send_message(chat_id=chat_id, text='Неправильный формат', reply_markup=None)


async def validation_str_to_time(time_list_str: list | str) -> List[time]:
    time_objects = []
    if isinstance(time_list_str, list):
        for t in time_list_str:
            hours, minutes = map(int, t.split(':'))
            time_obj = time(hours, minutes)
            time_objects.append(time_obj)

    else:
        hours, minutes = map(int, time_list_str.split(':'))
        time_obj = time(hours, minutes)
        time_objects.append(time_obj)

    return time_objects


