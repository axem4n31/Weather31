import httpx
import settings

client = httpx.AsyncClient()


async def get_coordinates_by_name(city_name: str):
    url = settings.GET_COORD_API + 'direct?q=' + city_name + '&limit=1'
    url += '&appid=' + settings.WEATHER_API_TOKEN
    response = await client.get(url, timeout=10)
    message = response.json()
    lat = message[0]['lat']
    lon = message[0]['lon']
    return lat, lon


async def get_temperature(lat, lon):
    url = settings.GET_TEMPERATURE + f"onecall?lat={lat}"
    url += f"&lon={lon}"
    url += f"&appid={settings.WEATHER_API_TOKEN}"
    response = await client.get(url, timeout=10)
    print(response.json())


