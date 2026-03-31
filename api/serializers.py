from rest_framework import serializers
from .models import (
    Category,
    Service,
    Appointment,
    Gallery,
    AboutSection,
    ContactMessage,
    Location,
    ServiceOption,
    Testimonial,
    Logo,
    Feedback
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = ["id", "duration", "price"]


class ServiceSerializer(serializers.ModelSerializer):
    options = ServiceOptionSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "category",
            "name",
            "image",
            "image_url",
            "description",
            "options",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.image_url or None

    def create(self, validated_data):
        options_data = self.initial_data.get("options", [])
        service = Service.objects.create(**validated_data)
        for option in options_data:
            ServiceOption.objects.create(service=service, **option)
        return service

    def update(self, instance, validated_data):
        options_data = self.initial_data.get("options", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.options.all().delete()
        for option in options_data:
            ServiceOption.objects.create(service=instance, **option)
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    service_option = serializers.PrimaryKeyRelatedField(
        queryset=ServiceOption.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "service",
            "service_option",
            "date",
            "time",
            "customer_name",
            "phone",
            "email",
            "notes",
            "payment_method",
            "transaction_id",
        ]
        read_only_fields = ["id", "transaction_id"]

    def create(self, validated_data):
        service_option = validated_data.pop("service_option", None)
        appointment = Appointment.objects.create(**validated_data)
        if service_option:
            appointment.service_option = service_option
            appointment.save()
        return appointment


class GallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ["id", "title", "image", "image_url", "created_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class AboutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutSection
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.unsplash_url or None


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class LogoSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Logo
        fields = ["id", "logo", "logo_url", "alt_text", "updated_at"]

    def get_logo_url(self, obj):
        request = self.context.get("request")
        if obj.logo and hasattr(obj.logo, "url"):
            return request.build_absolute_uri(obj.logo.url) if request else obj.logo.url
        return None


class FeedbackSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            "id",
            "name",
            "message",
            "profile_photo",
            "profile_photo_url",
            "created_at",
            "created_at_formatted",
        ]

    def get_profile_photo_url(self, obj):
        request = self.context.get("request")
        if obj.profile_photo and hasattr(obj.profile_photo, "url"):
            return request.build_absolute_uri(obj.profile_photo.url) if request else obj.profile_photo.url
        return None

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%B %d, %Y at %I:%M %p")
