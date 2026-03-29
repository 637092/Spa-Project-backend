from django.contrib import admin
from .models import Category, Service, Appointment, Gallery, AboutSection
from .models import ContactMessage, Logo

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Service, ServiceOption


admin.site.register(Category)


# 🔹 Inline for Service Options (price + duration)
class ServiceOptionInline(admin.TabularInline):
    model = ServiceOption
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "image_preview",
    )
    list_filter = ("category",)
    search_fields = ("name",)
    readonly_fields = ("image_preview",)

    inlines = [ServiceOptionInline]

    fieldsets = (
        ("Service Info", {
            "fields": ("category", "name", "description")
        }),
        ("Service Image", {
            "fields": ("image", "image_url", "image_preview"),
            "description": "Upload an image OR paste an image URL (Unsplash / CDN)."
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px;border-radius:8px;" />',
                obj.image.url
            )
        if obj.image_url:
            return format_html(
                '<img src="{}" style="height:80px;border-radius:8px;" />',
                obj.image_url
            )
        return "No Image"

    image_preview.short_description = "Preview"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "service",
        "date",
        "time",
        "status",
        "payment_method",
        "payment_status",
    )

    list_filter = (
        "status",
        "payment_method",
        "payment_status",
        "date",
    )

    search_fields = (
        "customer_name",
        "phone",
        "email",
        "transaction_id",
    )

    list_editable = (
        "status",
        "payment_status",
    )

    ordering = ("-date",)

    readonly_fields = (
        "transaction_id",
    )

    fieldsets = (
        ("Customer Info", {
            "fields": (
                "customer_name",
                "phone",
                "email",
                "notes",
            )
        }),
        ("Appointment Details", {
            "fields": (
                "service",
                "date",
                "time",
                "status",
            )
        }),
        ("Payment Details 💳", {
            "fields": (
                "payment_method",
                "payment_status",
                "transaction_id",
            )
        }),
    )

def payment_badge(self, obj):
    color = "orange"
    if obj.payment_status == "PAID":
        color = "green"
    elif obj.payment_status == "FAILED":
        color = "red"

    return f'<b style="color:{color}">{obj.payment_status}</b>'

payment_badge.allow_tags = True
payment_badge.short_description = "Payment"




@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title",)


@admin.register(AboutSection)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "type", "created_at")
    list_filter = ("type",)
    search_fields = ("name", "email", "message")


from .models import AdminContactInfo, Location

@admin.register(AdminContactInfo)
class AdminContactInfoAdmin(admin.ModelAdmin):
    list_display = ("email", "phone")

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "address", "is_active")
    search_fields = ("title", "address")

from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "company", "created_at")
    search_fields = ("name", "role", "company", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    # Optional: preview image in admin
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:50%;" />'
        return "No Image"

    image_preview.allow_tags = True
    image_preview.short_description = "Preview"


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ("alt_text", "logo_preview", "updated_at")
    readonly_fields = ("logo_preview", "created_at", "updated_at")

    fieldsets = (
        ("Logo Configuration", {
            "fields": ("logo", "logo_preview", "alt_text")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="height:100px;border-radius:8px;" />'
        return "No Logo"

    logo_preview.allow_tags = True
    logo_preview.short_description = "Preview"

    def has_add_permission(self, request):
        return not Logo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "message_preview", "profile_photo_preview", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "message")
    ordering = ("-created_at",)
    readonly_fields = ("profile_photo_preview", "created_at")

    fieldsets = (
        ("Feedback Details", {
            "fields": ("name", "message", "created_at")
        }),
        ("Profile Photo", {
            "fields": ("profile_photo", "profile_photo_preview"),
        }),
    )

    def message_preview(self, obj):
        # Truncate long messages for list view
        if len(obj.message) > 50:
            return obj.message[:50] + "..."
        return obj.message
    message_preview.short_description = "Message"

    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;border-radius:50%;object-fit:cover;border:2px solid #c9a44a;" />',
                obj.profile_photo.url
            )
        return "No Photo"
    profile_photo_preview.short_description = "Photo"