from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.db.models import Q
from api.models import Appointment
from api.utils.email import send_appointment_reminder_email


class Command(BaseCommand):
    help = "Send appointment reminder emails 1 hour before scheduled time"

    def handle(self, *args, **options):
        # Find appointments scheduled within the next hour
        current_time = now()
        one_hour_later = current_time + timedelta(hours=1)
        
        # ⏰ Check for appointments that are:
        # - Status: Confirmed or Pending
        # - Scheduled today/tomorrow
        # - Within next 60 minutes from current time
        today = current_time.date()
        
        upcoming_appointments = Appointment.objects.filter(
            Q(status="Confirmed") | Q(status="Pending"),
            date=today,
            time__gte=current_time.time(),
            time__lte=one_hour_later.time()
        )

        for appointment in upcoming_appointments:
            try:
                if appointment.email:
                    send_appointment_reminder_email(appointment)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Reminder sent to {appointment.customer_name} ({appointment.email})"
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Failed to send reminder for {appointment.customer_name}: {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Reminder check completed. {upcoming_appointments.count()} reminders sent."
            )
        )
