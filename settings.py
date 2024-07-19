from os import getenv
from dotenv import load_dotenv


load_dotenv()

TOKEN = getenv('TG_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/"
API_URL = getenv('XTUNNEL_URL')
WEBHOOK_SECRET_KEY = getenv('WEBHOOK_SECRET_KEY')
WEBHOOK_HANDLE_URL = API_URL + f'/handle_bot_events/{WEBHOOK_SECRET_KEY}/'
WEATHER_API = 'http://api.weatherapi.com/v1/'
WEATHER_API_TOKEN = getenv('WEATHER_API_TOKEN')

BROKER_URL = f"redis://{getenv('REDIS_HOST')}:6379"
