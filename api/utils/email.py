from django.core.mail import send_mail
from django.conf import settings


def send_booking_email(to_email, name, service, date, time):
    subject = "Appointment Confirmed – Elegant Thai Spa 🌿"

    message = f"""
Hello {name},

Your appointment has been successfully confirmed.

🧘 Service: {service}
📅 Date: {date}
⏰ Time: {time}

We look forward to welcoming you!

Warm regards,
Elegant Thai Spa
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_contact_email(contact):
    subject = f"📩 New Contact Message – {contact.name}"

    message = f"""
New contact message received:

👤 Name: {contact.name}
📧 Email: {contact.email}
📞 Phone: {contact.phone}

📝 Message:
{contact.message}
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )


def send_admin_booking_email(appointment):
    subject = f"📅 New Appointment Booking – {appointment.customer_name}"

    # Extract duration from notes
    duration = "N/A"
    if appointment.notes and "min" in appointment.notes:
        try:
            duration_part = appointment.notes.split("Package:")[1].split("min")[0].strip()
            duration = f"{duration_part} min"
        except:
            duration = "N/A"

    message = f"""
New appointment has been booked!

👤 Customer: {appointment.customer_name}
📧 Email: {appointment.email}
📞 Phone: {appointment.phone}

🧘 Service: {appointment.service.name}
⏱️ Duration: {duration}
📅 Date: {appointment.date}
⏰ Time: {appointment.time}

💳 Payment Method: {appointment.get_payment_method_display()}
📝 Notes: {appointment.notes or "None"}

Status: {appointment.status}
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )


def send_status_notification_email(appointment, status):
    """Send email to customer when status is changed to Completed or Cancelled"""
    if status == "Completed":
        subject = "✅ Appointment Completed – Thank You!"
        message = f"""
Hello {appointment.customer_name},

Your appointment has been completed! We hope you enjoyed our service.

🧘 Service: {appointment.service.name}
📅 Date: {appointment.date}
⏰ Time: {appointment.time}

Thank you for choosing Elegant Thai Spa. We look forward to seeing you again!

Warm regards,
Elegant Thai Spa
"""
    elif status == "Cancelled":
        subject = "❌ Appointment Cancelled"
        message = f"""
Hello {appointment.customer_name},

Your appointment has been cancelled.

🧘 Service: {appointment.service.name}
📅 Date: {appointment.date}
⏰ Time: {appointment.time}

If you have any questions, feel free to contact us.

Regards,
Elegant Thai Spa
"""
    else:
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        fail_silently=False,
    )


def send_appointment_reminder_email(appointment):
    """Send reminder email 1 hour before appointment"""
    subject = "⏰ Appointment Reminder – Elegant Thai Spa"

    # Extract duration and price from notes
    duration = "N/A"
    price = "N/A"
    if appointment.notes and "Package:" in appointment.notes:
        try:
            package_part = appointment.notes.split("Package:")[1]
            duration_match = package_part.split("min")[0].strip()
            price_match = package_part.split("₹")[1].split("\n")[0] if "₹" in package_part else "N/A"
            duration = f"{duration_match} min"
            price = f"₹{price_match}"
        except:
            pass

    message = f"""
Hello {appointment.customer_name},

This is a friendly reminder about your upcoming appointment!

🧘 Service: {appointment.service.name}
⏱️ Duration: {duration}
💰 Price: {price}
📅 Date: {appointment.date}
⏰ Time: {appointment.time}

📍 Location: [Visit our website for location details]

Please arrive 10 minutes early. If you need to reschedule or cancel, please let us know as soon as possible.

We look forward to welcoming you!

Warm regards,
Elegant Thai Spa
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        fail_silently=False,
    )

