import json

import httpx
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from models.model import User
from models.model_settings import db_helper

client = httpx.AsyncClient()


async def send_message(chat_id: int, text: str, reply_markup: None | dict):
    url = settings.TELEGRAM_API_URL + 'sendMessage'
    reply_markup_json = json.dumps(reply_markup)
    params = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup_json
    }

    response = await client.post(url, data=params)
    print(response.json())


async def check_user_location(user_tg_id: int, db: AsyncSession):
    user = await db.scalar(select(User).where(and_(User.user_tg_id == user_tg_id)))
    if user:
        return True
    return False


async def get_user_coordinates(user_tg_id: int, db: AsyncSession):
    user = await db.scalar(select(User).where(and_(User.user_tg_id == user_tg_id)))
    lat = user.lat
    lon = user.lon
    return lat, lon


