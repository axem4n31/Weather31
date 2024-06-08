import httpx
import settings
from models.schemas import WeatherSchema

client = httpx.AsyncClient()


async def get_city_coordinates(city_name: str):
    url = settings.GET_COORD_API + 'direct?q=' + city_name + '&limit=1'
    url += '&appid=' + settings.COORD_API_TOKEN
    response = await client.get(url, timeout=10)
    message = response.json()
    if message is None:
        return None
    lat = message[0]['lat']
    lon = message[0]['lon']
    return lat, lon


async def get_current_weather(lat, lon):

    url = settings.BASE_TEMPERATURE_API + 'current.json'
    url += '?key=' + settings.WEATHER_API_TOKEN
    url += f"&q={lat},{lon}"
    response = await client.get(url, timeout=10)
    weather_data = response.json()
    print(weather_data)
    weather = WeatherSchema(
        city=weather_data['location']['name'],
        region=weather_data['location']['region'],
        country=weather_data['location']['country'],
        feels_like=weather_data['current']['feelslike_c'],
        temp=weather_data['current']['temp_c'],
        cloud=weather_data['current']['cloud'],
        uv=weather_data['current']['uv'],
        speed_wind=weather_data['current']['wind_kph'],
        gust_wind=weather_data['current']['gust_kph']
    )
    return weather
