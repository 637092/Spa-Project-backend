import requests
from django.conf import settings
import json


def send_whatsapp_message(phone, name, service, date, time):
    url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "appointment_confirmation",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": name},
                        {"type": "text", "text": service},
                        {"type": "text", "text": str(date)},
                        {"type": "text", "text": str(time)},
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


# 🔥 NEW: Status change notification WhatsApp
def send_status_notification_whatsapp(phone, name, status):
    url = f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    if status == "Completed":
        message_text = f"Hi {name}, your appointment has been completed! Thank you for choosing Elegant Thai Spa. We hope to see you soon! 🧘"
    elif status == "Cancelled":
        message_text = f"Hi {name}, your appointment has been cancelled. If you have any questions, please contact us. 📞"
    else:
        return

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
