from fastapi import APIRouter, HTTPException
from app.weather_services import get_city_coordinates, get_weather
from models.schemas import WeatherSchema

api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.get('/find_out_the_weather/{city:str, days:int}')
async def find_out_the_weather_router(city: str, days: int = 1) -> WeatherSchema | None:
    """
    Get weather forecast by city name.
    city - City name.
    days - Number of days in the forecast (default is 1).
    Returns weather data upon successful request. Returns None otherwise.
    """
    try:
        # Получаем координаты города
        coord = await get_city_coordinates(city_name=city)
        if coord is None:
            return
        # Получаем данные о погоде
        data = await get_weather(lat=coord.lat, lon=coord.lon, days=days)

        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error : {e}"
        )
