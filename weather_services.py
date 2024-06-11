import httpx
import settings
from models.schemas import WeatherSchema, CoordinatesSchema, Days

client = httpx.AsyncClient()


async def get_city_coordinates(city_name: str) -> CoordinatesSchema | None:
    url = settings.GET_COORD_API + 'direct?q=' + city_name + '&limit=1'
    url += '&appid=' + settings.COORD_API_TOKEN
    response = await client.get(url, timeout=10)
    message = response.json()
    print(message)
    if not message:
        return None
    return CoordinatesSchema(city=message[0]['name'],
                             country=message[0]['country'],
                             lat=message[0]['lat'],
                             lon=message[0]['lon'])


async def get_weather(lat: float, lon: float, days: int):
    url = settings.BASE_TEMPERATURE_API + 'forecast.json'
    url += '?key=' + settings.WEATHER_API_TOKEN
    url += f"&q={lat},{lon}" + f"&days={days}" + '&lang=ru'
    response = await client.get(url, timeout=10)
    weather_data = response.json()
    print(weather_data)
    region = None
    if 'state' in weather_data['location']:
        region = weather_data['location']['state']

    # Создаем список для хранения данных о днях
    daily_forecasts = []

    # Извлекаем прогнозы на каждый день из данных
    for forecast in weather_data['forecast']['forecastday'][:days]:
        # Создаем объект Days с помощью данных из прогноза
        daily_forecast = Days(
            date=forecast['date'],
            max_temp=forecast['day']['maxtemp_c'],
            min_temp=forecast['day']['mintemp_c'],
            daily_chance_of_rain=int(forecast['day']['daily_chance_of_rain']),
            max_wind_kph=forecast['day']['maxwind_kph'],
            uv=int(forecast['day']['uv']),
            text=forecast['day']['condition']['text'],
        )
        # Добавляем объект Days в список daily_forecasts
        daily_forecasts.append(daily_forecast)

    # Создаем объект WeatherSchema с общими данными о погоде и списком daily_forecasts
    weather = WeatherSchema(
        city=weather_data['location']['name'],
        region=weather_data['location']['region'],
        country=weather_data['location']['country'],
        feels_like=weather_data['current']['feelslike_c'],
        temp=weather_data['current']['temp_c'],
        cloud=weather_data['current']['cloud'],
        uv=weather_data['current']['uv'],
        speed_wind=weather_data['current']['wind_kph'],
        gust_wind=weather_data['current']['gust_kph'],
        humidity=weather_data['current']['humidity'],
        text=weather_data['current']['condition']['text'],
        days=daily_forecasts
    )

    return weather
