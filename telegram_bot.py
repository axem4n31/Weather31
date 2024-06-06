import settings
import httpx

client = httpx.AsyncClient()

# временный файл для настройки конфигурации кнопки


async def send_message(chat_id: int):
    url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': 'Выберите действие:',
        'reply_markup': '{"keyboard":[[{"text": "Текущая погода"}, '
                        '{"text": "Настройки"}],[{"text": "Уведомления"}, '
                        '{"text": "Помощь"}]], "resize_keyboard":true}'
    }
    response = await client.post(url, data=params)
    print(response.json())
