from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from .utils.whatsapp import send_whatsapp_message
from .utils.email import send_admin_booking_email


@receiver(post_save, sender=Appointment)
def send_whatsapp_on_booking(sender, instance, created, **kwargs):
    if created:
        phone = instance.phone.strip().replace("+", "")
        if not phone.startswith("91"):
            phone = "91" + phone

        send_whatsapp_message(
            phone=phone,
            name=instance.customer_name,
            service=instance.service.name,
            date=instance.date,
            time=instance.time
        )

        # 🔥 ADDED: Send admin notification email
        send_admin_booking_email(instance)
