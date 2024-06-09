import httpx
import settings
from models.schemas import WeatherSchema, CoordinatesSchema

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


async def get_weather(lat: float, lon: float):
    url = settings.BASE_TEMPERATURE_API + 'forecast.json'
    url += '?key=' + settings.WEATHER_API_TOKEN
    url += f"&q={lat},{lon}" + '&days=1' + '&lang=ru'
    response = await client.get(url, timeout=10)
    weather_data = response.json()
    print(weather_data)
    region = None
    if 'state' in weather_data['location']:
        region = weather_data['location']['state']
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
    )
    return weather
