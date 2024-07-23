import httpx
from httpx import AsyncClient
import settings


async def set_webhook():
    try:
        url = settings.TELEGRAM_API_URL + "setWebhook"
        url += "?url=" + settings.WEBHOOK_HANDLE_URL
        url += '&allowed_updates=["message"'
        url += ', "callback_query"]'
        async with AsyncClient() as client:
            response = await client.post(url, timeout=10)
        print('Webhook set with response:', response.json())
    except Exception as e:
        print(f"Error set_webhook : {e}")


async def remove_webhook():
    try:
        async with AsyncClient() as client:
            response = await client.post(settings.TELEGRAM_API_URL + "setWebhook?remove=", timeout=10)
        print('Webhook deleted with response:', response.json())
    except httpx.ConnectTimeout as e:
        print(f"Error remove_webhook : {e}")
