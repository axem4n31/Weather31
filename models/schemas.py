from typing import List

from pydantic import BaseModel


class Days(BaseModel):
    date: str  # Дата
    max_temp: float  # Максимальная температура
    min_temp: float  # Минимальня температура
    daily_chance_of_rain: int  # Процент вероятности дождя
    max_wind_kph: float  # Максимальная скорость ветра
    uv: int  # Индекс ультрофиолета
    text: str  # Описание


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
    humidity: int  # процент влажности
    text: str  # Описание
    days: List[Days]


class CoordinatesSchema(BaseModel):
    city: str
    country: str
    lat: float
    lon: float


class CityList(BaseModel):
    cities: List[CoordinatesSchema]


