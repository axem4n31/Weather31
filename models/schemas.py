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


class CoordinatesSchema(BaseModel):
    lat: float
    lon: float
