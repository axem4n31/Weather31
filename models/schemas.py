from typing import List

from pydantic import BaseModel


class WeatherSchema(BaseModel):
    city: str  # Название города
    region: str  # Название региона
    country: str  # Название страны
    feels_like: float  # Ощущается как
    temp: float  # Фактическая температура
    cloud: int  # Процент облачности
    uv: int  # Индекс ультрофиолета
    speed_wind: float  # Скорость ветра
    gust_wind: float  # Порыв ветра
    humidity: int  #процент влажности
    text: str  # Описание


class CoordinatesSchema(BaseModel):
    city: str
    country: str
    lat: float
    lon: float


class CityList(BaseModel):
    cities: List[CoordinatesSchema]
