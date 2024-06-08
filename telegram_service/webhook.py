import httpx
import settings

client = httpx.AsyncClient()


async def set_webhook():
    url = settings.TELEGRAM_API_URL + "setWebhook"
    url += "?url=" + settings.WEBHOOK_HANDLE_URL
    url += '&allowed_updates=["message"'
    url += ', "callback_query"]'
    response = await client.post(url, timeout=10)
    print('Webhook set with response:', response.json())


async def remove_webhook():
    response = await client.post(settings.TELEGRAM_API_URL + "setWebhook?remove=", timeout=10)
    print('Webhook deleted with response:', response.json())
