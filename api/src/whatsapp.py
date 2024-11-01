from .settings import app_settings as settings
import requests

def send_whatsapp_message(user_number, message):
    api_a_url = f"{settings.WHATSAPP_API_URL}/send/message"
    payload = {
        'phone': f'{user_number}@s.whatsapp.net',
        'message': message
    }
    response = requests.post(api_a_url, json=payload)
    return response.json()