from django.conf import settings
import requests

def send_whatsapp_message(phoneNumber, message):
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}
    payload = {"messaging_product": "whatsapp",
                "recipent_type":"individual",
                "to": phoneNumber,
                "type": "text",
                "text": {"body": message}
                }

    response = requests.post(url, headers=headers, json=payload)
    ans = response.json()
    return ans