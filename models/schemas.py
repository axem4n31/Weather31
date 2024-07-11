from typing import List

from pydantic import BaseModel
from datetime import time


class HourSchema(BaseModel):
    time: str
    temp: float
    feels_like: float
    humidity: int
    cloud: int
    wind_kph: float
    chance_of_rain: int
    text: str


class DaysSchema(BaseModel):
    is_day: int  # Номер дня в массиве
    date: str  # Дата
    max_temp: float  # Максимальная температура
    min_temp: float  # Минимальня температура
    daily_chance_of_rain: int  # Процент вероятности дождя
    max_wind_kph: float  # Максимальная скорость ветра
    uv: int  # Индекс ультрофиолета
    text: str  # Описание
    hours: List[HourSchema]


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
    days: List[DaysSchema]


class CoordinatesSchema(BaseModel):
    city: str | None
    country: str | None
    lat: float
    lon: float


class CityList(BaseModel):
    cities: List[CoordinatesSchema]


class NotificationSchema(BaseModel):
    chat_id: int
    utc: str
    time: List[time] = None
