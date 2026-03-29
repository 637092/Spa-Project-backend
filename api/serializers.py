from rest_framework import serializers
from .models import Category, Service, Appointment, Gallery, AboutSection, ContactMessage, Location


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


from rest_framework import serializers
from .models import Service, ServiceOption


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = ["id", "duration", "price"]


# ✅ NEW MAIN SERIALIZER (WITH OPTIONS)
class ServiceSerializer(serializers.ModelSerializer):
    options = ServiceOptionSerializer(many=True, read_only=True)

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

    # CREATE with nested options
    def create(self, validated_data):
        options_data = self.initial_data.get('options', [])
        service = Service.objects.create(**validated_data)

        for option in options_data:
            ServiceOption.objects.create(service=service, **option)

        return service

    # UPDATE with nested options
    def update(self, instance, validated_data):
        options_data = self.initial_data.get('options', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.options.all().delete()

        for option in options_data:
            ServiceOption.objects.create(service=instance, **option)

        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "service",
            "date",
            "time",
            "customer_name",
            "phone",
            "email",
            "notes",
            "payment_method",
            "transaction_id",
        ]

        read_only_fields = [
            "id",
            "transaction_id",
        ]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class AboutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutSection
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return obj.unsplash_url


# ⚠️ OLD SERIALIZER (RENAMED TO AVOID CONFLICT)
class ServiceSerializerOld(serializers.ModelSerializer):
    image_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            # ❌ removed price & duration (to prevent crash)
            "description",
            "image",
            "image_url",
            "image_display",
        ]

    def get_image_display(self, obj):
        if obj.image:
            return obj.image.url
        return obj.image_url


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


from rest_framework import serializers
from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


from rest_framework import serializers
from .models import Logo


class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'logo', 'alt_text', 'updated_at']


from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'message', 'profile_photo', 'profile_photo_url', 'created_at', 'created_at_formatted']

    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%B %d, %Y at %I:%M %p")