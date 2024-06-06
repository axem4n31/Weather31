import httpx
import settings

client = httpx.AsyncClient()


async def get_coordinates_by_name(city_name: str):
    url = settings.GET_COORD_API + 'direct?q=' + city_name + '&limit=1'
    url += '&appid=' + settings.COORD_API_TOKEN
    response = await client.get(url, timeout=10)
    message = response.json()
    lat = message[0]['lat']
    lon = message[0]['lon']
    return lat, lon


async def get_temperature(lat, lon):
    url = settings.BASE_TEMPERATURE_API + 'current.json'
    url += '?key=' + settings.WEATHER_API_TOKEN
    url += f"&q={lat},{lon}"
    response = await client.get(url, timeout=10)
    message = response.json()
    print(message)
    print(message['current']['temp_c'])


