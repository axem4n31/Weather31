from os import getenv
from dotenv import load_dotenv


load_dotenv()

TOKEN = getenv('TG_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/"
API_URL = getenv('XTUNNEL_URL')
WEBHOOK_SECRET_KEY = getenv('WEBHOOK_SECRET_KEY')
WEBHOOK_HANDLE_URL = API_URL + f'/handle_bot_events/{WEBHOOK_SECRET_KEY}/'
COORD_API_TOKEN = getenv('COORD_API_TOKEN')
GET_COORD_API = 'http://api.openweathermap.org/geo/1.0/'
BASE_TEMPERATURE_API = 'http://api.weatherapi.com/v1/'
WEATHER_API_TOKEN = getenv('WEATHER_API_TOKEN')


help_text = "/start - узнать текущую погоду" \
                "\n/forecast - узнать прогноз погоды" \
                "\n/change_region - изменить регион" \
                "\n/notifications - настройка уведомлений" \
                "\nЕсли у вас есть жалобы или предложения" \
                "\nпишите нам ibdcorporation31@gmail.com"

not_found_city_text = 'Город не найден, введите корректное наименование.' \
           '\nДля большей информации воспользуйтесь командой /help'

location_text = "Для получения информации о погоде, пожалуйста, " \
           "укажите название города (напишите его в чат) или поделитесь геолокацией"
