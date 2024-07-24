from fastapi import APIRouter, HTTPException
from app.weather_services import get_city_coordinates, get_weather, check_token
from models.schemas import WeatherSchema, GetWeatherSchema, CoordinatesSchema

api_router = APIRouter(prefix="/api", tags=["API"])
# @api_router.get('/find_out_the_weather/{city:str, days:int}')
# async def find_out_the_weather_router(city: str, days: int = 1) -> WeatherSchema | None:


@api_router.post('/find_out_the_weather')
async def find_out_the_weather_router(data: GetWeatherSchema) -> WeatherSchema | None:
    """
    Get weather forecast by city name.
    city - City name.
    days - Number of days in the forecast (default is 1).
    Returns weather data upon successful request. Returns None otherwise.
    """
    await check_token(token=data.token)

    try:
        coord = CoordinatesSchema
        if isinstance(data.city, list):
            coord = data.city[0]
        if isinstance(data.city, str):
            # Получаем координаты города
            coord = await get_city_coordinates(city_name=data.city)
            if coord is None:
                return
        # Получаем данные о погоде
        data = await get_weather(lat=coord.lat, lon=coord.lon, days=data.days)

        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error : {e}"
        )
