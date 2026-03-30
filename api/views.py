from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Category, Service, Appointment, Gallery, AboutSection, Testimonial, Logo, AdminContactInfo, Location
from .serializers import CategorySerializer, ServiceSerializer, AppointmentSerializer, GallerySerializer, AboutSerializer, TestimonialSerializer, LogoSerializer, LocationSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .utils.whatsapp import send_whatsapp_message
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .utils.email import send_booking_email
from .utils.email import send_contact_email
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Service
from .serializers import ServiceSerializer





class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS



class ServiceListView(ListAPIView):
    queryset = Service.objects.all().prefetch_related('options')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}


class ServiceDetailView(RetrieveAPIView):
    queryset = Service.objects.all().prefetch_related('options')
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}

from rest_framework.response import Response
from rest_framework import status


from rest_framework.response import Response
from rest_framework import status


class AppointmentCreateView(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_method = serializer.validated_data.get(
            "payment_method", "PAY_AT_SERVICE"
        )

        appointment = serializer.save(
            user=request.user if request.user.is_authenticated else None,
            status="Confirmed",
            payment_status="PENDING"
        )

        # ✅ SEND RESPONSE IMMEDIATELY (FAST UX)
        response = Response(serializer.data, status=status.HTTP_201_CREATED)

        # ---------------- PHONE FORMAT ----------------
        try:
            phone = appointment.phone.strip().replace("+", "")
            if not phone.startswith("91"):
                phone = "91" + phone

            # ---------------- WHATSAPP ----------------
            send_whatsapp_message(
                phone=phone,
                name=appointment.customer_name,
                service=appointment.service.name,
                date=appointment.date,
                time=appointment.time
            )

            # ---------------- EMAIL ----------------
            if appointment.email:
                send_booking_email(
                    to_email=appointment.email,
                    name=appointment.customer_name,
                    service=appointment.service.name,
                    date=appointment.date,
                    time=appointment.time
                )
        except Exception as e:
            print("⚠️ Notification error:", e)

        return response

class PaymentVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        appointment_id = request.data.get("appointment_id")
        transaction_id = request.data.get("transaction_id")

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.payment_status = "PAID"
            appointment.transaction_id = transaction_id
            appointment.save()

            return Response({"message": "Payment verified"})
        except Appointment.DoesNotExist:
            return Response({"error": "Invalid appointment"}, status=404)

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RazorpayKeyAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "key": settings.RAZORPAY_KEY_ID
        })



class GalleryListView(ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_serializer_context(self):
        return {"request": self.request}


class AboutAPIView(ListAPIView):
    queryset = AboutSection.objects.filter(is_active=True)
    serializer_class = AboutSerializer

    def get_serializer_context(self):
        return {"request": self.request}

class AppointmentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        status_value = request.data.get("status")

        if status_value not in ["Pending", "Confirmed", "Completed", "Cancelled"]:
            return Response({"error": "Invalid status"}, status=400)

        old_status = appointment.status
        appointment.status = status_value
        appointment.save()

        # 🔥 ADDED: Send notifications on status change
        if status_value in ["Completed", "Cancelled"] and appointment.email and appointment.phone:
            from .utils.email import send_status_notification_email
            from .utils.whatsapp import send_status_notification_whatsapp
            
            try:
                send_status_notification_email(appointment, status_value)
            except Exception as e:
                print(f"Email notification failed: {e}")
            
            try:
                phone = appointment.phone.strip().replace("+", "")
                if not phone.startswith("91"):
                    phone = "91" + phone
                send_status_notification_whatsapp(phone, appointment.customer_name, status_value)
            except Exception as e:
                print(f"WhatsApp notification failed: {e}")

        return Response({"message": "Status updated"})

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Max
from django.utils.timezone import now
from datetime import timedelta, date
from decimal import Decimal
import re

class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def parse_price(self, notes):
        if not notes:
            return Decimal("0")
        match = re.search(r"₹\s*([0-9]+(?:\.[0-9]+)?)", notes)
        if match:
            try:
                return Decimal(match.group(1))
            except Exception:
                return Decimal("0")
        return Decimal("0")

    def compute_earnings(self, queryset):
        total = Decimal('0')

        for appointment in queryset:
            # Use explicit price if available on model
            amount = Decimal('0')
            if getattr(appointment, 'price', None):
                try:
                    amount = Decimal(appointment.price)
                except Exception:
                    amount = Decimal('0')

            # parse from notes if needed
            if amount <= 0:
                amount = self.parse_price(appointment.notes)

            # fallback to service option max-priced option
            if amount <= 0 and appointment.service:
                option = appointment.service.options.order_by('-price').first()
                if option and option.price:
                    amount = Decimal(option.price)

            total += amount

        return total

    def percent_diff(self, current, previous):
        if previous == 0:
            if current == 0:
                return 0.0
            return 100.0
        try:
            return float(((current - previous) / previous) * 100)
        except Exception:
            return None

    def get(self, request):
        today = now().date()
        this_month_start = today.replace(day=1)
        this_year_start = today.replace(month=1, day=1)

        prev_day = today - timedelta(days=1)
        last_month_end = this_month_start - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        last_year_start = this_year_start.replace(year=this_year_start.year - 1)
        last_year_end = this_year_start - timedelta(days=1)

        # Keep completed count separate for cards, but revenue uses both confirmed+completed
        completed = Appointment.objects.filter(status="Completed")
        revenue_queryset = Appointment.objects.filter(status__in=["Confirmed", "Completed"])

        today_earnings = self.compute_earnings(revenue_queryset.filter(date=today))
        month_earnings = self.compute_earnings(revenue_queryset.filter(date__year=today.year, date__month=today.month))
        year_earnings = self.compute_earnings(revenue_queryset.filter(date__year=today.year))

        prev_day_earnings = self.compute_earnings(revenue_queryset.filter(date=prev_day))
        prev_month_earnings = self.compute_earnings(revenue_queryset.filter(date__year=last_month_start.year, date__month=last_month_start.month))
        prev_year_earnings = self.compute_earnings(revenue_queryset.filter(date__year=last_year_start.year))

        day_pct = self.percent_diff(today_earnings, prev_day_earnings)
        month_pct = self.percent_diff(month_earnings, prev_month_earnings)
        year_pct = self.percent_diff(year_earnings, prev_year_earnings)

        if day_pct is not None and day_pct > 0:
            day_trend = f"Daily revenue is up {day_pct:.1f}% compared to yesterday."
        elif day_pct is not None and day_pct < 0:
            day_trend = f"Daily revenue is down {abs(day_pct):.1f}% compared to yesterday."
        else:
            day_trend = "Daily comparison is not available yet (base day zero)."

        if month_pct is not None and month_pct > 0:
            month_trend = f"Monthly revenue is up {month_pct:.1f}% compared to last month."
        elif month_pct is not None and month_pct < 0:
            month_trend = f"Monthly revenue is down {abs(month_pct):.1f}% compared to last month."
        else:
            month_trend = "Monthly comparison is not available yet (base month zero)."

        if year_pct is not None and year_pct > 0:
            year_trend = f"Yearly revenue is up {year_pct:.1f}% compared to last year."
        elif year_pct is not None and year_pct < 0:
            year_trend = f"Yearly revenue is down {abs(year_pct):.1f}% compared to last year."
        else:
            year_trend = "Yearly comparison is not available yet (base year zero)."

        trend_message = (
            f"{day_trend} {month_trend} {year_trend} "
            f"Focus on repeat customer experience and upsells to improve business performance."
        )

        if day_pct is None:
            day_pct = 0.0
        if month_pct is None:
            month_pct = 0.0
        if year_pct is None:
            year_pct = 0.0

        return Response({
            "total": Appointment.objects.count(),
            "today": Appointment.objects.filter(date=today).count(),
            "pending": Appointment.objects.filter(status="Pending").count(),
            "confirmed": Appointment.objects.filter(status="Confirmed").count(),
            "completed": completed.count(),
            "cancelled": Appointment.objects.filter(status="Cancelled").count(),
            "today_earnings": float(today_earnings),
            "month_earnings": float(month_earnings),
            "year_earnings": float(year_earnings),
            "total_earnings": float(self.compute_earnings(completed)),
            "day_pct": float(day_pct),
            "month_pct": float(month_pct),
            "year_pct": float(year_pct),
            "trend_message": trend_message,
            "trend_data": {
                "today": float(today_earnings),
                "previous_day": float(prev_day_earnings),
                "month": float(month_earnings),
                "previous_month": float(prev_month_earnings),
                "year": float(year_earnings),
                "previous_year": float(prev_year_earnings),
            },
            "recent": Appointment.objects.order_by("-id")[:5].values(
                "id",
                "customer_name",
                "phone",
                "email",
                "service__name",
                "date",
                "time",
                "status",
                "notes"
            )
        })

class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user or not user.is_staff:
            return Response(
                {"error": "Invalid admin credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
        })

from rest_framework_simplejwt.tokens import RefreshToken

class AdminLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Admin logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
from .models import ContactMessage
from .serializers import ContactSerializer

class ContactCreateView(CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save()
        print("📩 New contact message from:", contact.email)
        send_contact_email(contact)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import AdminContactInfo

class AdminContactInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        info = AdminContactInfo.objects.first()
        if not info:
            return Response({
                "email": "",
                "phone": "",
                "address": ""
            })

        return Response({
            "email": info.email,
            "phone": info.phone,
            "address": info.address,
        })

class LocationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        location = Location.objects.filter(is_active=True).first() or Location.objects.first()
        if not location:
            return Response({
                "title": "Visit Us",
                "address": "K-5, Kalinga Vihar LIG, Kalinganagar, Bhubaneswar, Odisha – 751028",
                "opening_days": "Monday – Sunday",
                "opening_time": "10:00 AM",
                "closing_time": "09:00 PM",
                "map_query": "K-5, Kalinga Vihar LIG, Kalinganagar, Bhubaneswar, Odisha 751028",
                "map_embed_url": ""
            })

        class FeedbackListCreateView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .ai_engine import get_ai_reply


class AIChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("✅ AI CHAT HIT")

        message = request.data.get("message", "")
        print("📩 MESSAGE:", message)

        if not message.strip():
            return Response({"error": "Message is required"}, status=400)

        try:
            response = get_ai_reply(message)
            print("🤖 RAW AI RESPONSE:", response)

            # 🔹 NORMALIZE RESPONSE (key fix)
            if isinstance(response, dict):
                # ensure `reply` always exists for frontend safety
                response.setdefault("reply", "")
                return Response(response)

            # fallback (should not happen, but safe)
            return Response({
                "type": "text",
                "reply": str(response)
            })

        except Exception as e:
            print("❌ AI VIEW ERROR:", e)
            return Response(
                {
                    "type": "text",
                    "reply": "⚠️ Sorry, something went wrong. Please try again later."
                },
                status=500
            )

from rest_framework.permissions import AllowAny

class TestimonialListView(ListAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]   # ✅ ADD THIS

class LogoRetrieveView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logo = Logo.objects.first()
        if logo:
            serializer = LogoSerializer(logo, context={"request": request})
            return Response(serializer.data)
        else:
            return Response({
                "id": None,
                "logo": None,
                "alt_text": "Elegant Thai Spa Logo"
            })


from rest_framework.generics import ListCreateAPIView
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackListCreateView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
