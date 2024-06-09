from fastapi import APIRouter, Request, Depends
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_settings import db_helper
from telegram_service.handly_event import handle_bot_events
from weather_services import get_city_coordinates, get_weather

event_router = APIRouter(prefix="/handle_bot_events", tags=["Handle events"])
api_router = APIRouter(prefix="/api", tags=["API"])

client = httpx.AsyncClient()

@event_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str,
                                   db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    await handle_bot_events(request=request, secret_key=secret_key, db=db)


@api_router.post('/find_out_the_weather')
async def find_out_the_weather_router(city: str):
    # тестовый роутер для проверки стороннего API без использования telegram
    # получение долготы широты по наименованию города
    coord = await get_city_coordinates(city_name=city)
    data = await get_weather(lat=coord.lat, lon=coord.lon)
    return data


