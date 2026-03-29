import re
from django.apps import apps

BASE_FRONTEND_URL = "http://localhost:3000"



def get_services_reply():
    Service = apps.get_model("api", "Service")
    services = Service.objects.all()

    if not services.exists():
        return {
            "type": "text",
            "reply": "⚠️ Currently, no services are available."
        }

    return {
        "type": "services",
        "services": [
            {
                "id": service.id,
                "name": service.name,
                "price": float(service.price),
                "duration": service.duration
            }
            for service in services
        ]
    }


def get_ai_reply(message: str):
    msg = message.lower().strip()

    if re.search(r"\b(hi|hello|hey|hii)\b", msg):
        return {
            "type": "text",
            "reply": (
                "👋 Hello! Welcome to Elegant International Thai Spa & Salon.\n"
                "How can I assist you today? 😊"
            )
        }

    if "service" in msg or "massage" in msg or "spa" in msg:
        return get_services_reply()

    if "book" in msg or "appointment" in msg:
        return {
            "type": "text",
            "reply": (
                "📅 Please choose a service below to book an appointment."
            )
        }

    return {
        "type": "text",
        "reply": (
            "🤖 I can help you with services, bookings, or general inquiries."
        )
    }

