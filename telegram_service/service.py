import json
from typing import Tuple
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
