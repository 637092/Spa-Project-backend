from django.urls import path
from .views import (
    CategoryListView, ServiceListView, AppointmentCreateView,
    GalleryListView, AboutAPIView, ServiceDetailView,
    AppointmentStatusUpdateView, AdminDashboardStatsAPIView,
    AdminLoginAPIView, ContactCreateView, TestimonialListView,
    LogoRetrieveView, AdminContactInfoAPIView, LocationAPIView,
    AIChatAPIView, RazorpayKeyAPIView, PaymentVerifyAPIView,
    FeedbackListCreateView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("services/", ServiceListView.as_view()),
    path("services/<int:pk>/", ServiceDetailView.as_view()),
    path("appointments/", AppointmentCreateView.as_view()),
    path("appointments/<int:pk>/status/", AppointmentStatusUpdateView.as_view()),
    path("gallery/", GalleryListView.as_view()),
    path("about/", AboutAPIView.as_view()),
    path("admin/dashboard/", AdminDashboardStatsAPIView.as_view()),
    path("admin/login/", AdminLoginAPIView.as_view()),
    path("contact/", ContactCreateView.as_view()),
    path("ai/chat/", AIChatAPIView.as_view()),
    path("admin-contact/", AdminContactInfoAPIView.as_view()),
    path("location/", LocationAPIView.as_view()),
    path("razorpay-key/", RazorpayKeyAPIView.as_view()),
    path("payment/verify/", PaymentVerifyAPIView.as_view()),
    path("testimonials/", TestimonialListView.as_view(), name="testimonials"),
    path("logo/", LogoRetrieveView.as_view(), name="logo"),
    path("feedback/", FeedbackListCreateView.as_view(), name="feedback"),
]

# ✅ Add this safely
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
