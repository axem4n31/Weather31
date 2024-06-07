import settings
import httpx

from service import send_message

client = httpx.AsyncClient()


async def start_event(message):
    chat_id = int(message['message']['chat']['id'])
    text = "Для получения информации о погоде, пожалуйста, укажите название города (напишите его в чат) или поделитесь геолокацией"
    url = settings.TELEGRAM_API_URL + 'fd'
    reply_markup = {
        "keyboard": [
            [{"text": "Текущая погода 🌡️", "request_location": True}],
            [{"text": "Прогноз погоды 🌤️"}],
            [{"text": "Уведомления 🔔"}, {"text": "Изменить регион 🌍"}, {"text": "Помощь 🆘"}]
        ],
        "resize_keyboard": True
    }
    reply_markup_2 = {
        "inline_keyboard": [
            [{"text": "Поделиться геолокацией", "callback_data": "share_location"}]
            ]
    }
    # временный словари
    await send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


