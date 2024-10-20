import requests
from django.conf import settings

def send_telegram_message(telegram_id, message):
    BOT_TOKEN= settings.BOT_TOKEN
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': telegram_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()