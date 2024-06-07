from fastapi import APIRouter, Request
import httpx
from handly_event import handle_bot_events
from service import get_coordinates_by_name, get_temperature


event_router = APIRouter(prefix="/handle_bot_events", tags=["Handle events"])
api_router = APIRouter(prefix="/api", tags=["API"])

client = httpx.AsyncClient()

@event_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str):
    await handle_bot_events(request=request, secret_key=secret_key)


@api_router.post('/find_out_the_weather')
async def find_out_the_weather_router(city: str):
    # тестовый роутер для проверки стороннего API без использования telegram
    # получение долготы широты по наименованию города
    lat, lon = await get_coordinates_by_name(city_name=city)
    await get_temperature(lat=lat, lon=lon)


