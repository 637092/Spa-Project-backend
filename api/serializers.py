from rest_framework import serializers
from .models import Category, Service, Appointment, Gallery, AboutSection, ContactMessage, Location
from .models import ServiceOption
from .models import Testimonial
from .models import Logo
from .models import Feedback


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


# ✅ MAIN SERVICE SERIALIZER (FIXED IMAGE URL)
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
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None

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
    service_option = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "service",
            "service_option",   # ✅ ADD THIS
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

    def create(self, validated_data):
        validated_data.pop("service_option", None)  # ✅ IGNORE SAFELY
        return super().create(validated_data)


class GallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None


class AboutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AboutSection
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return obj.unsplash_url


# ⚠️ OLD SERIALIZER (kept same, only fixed URL)
class ServiceSerializerOld(serializers.ModelSerializer):
    image_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "image",
            "image_url",
            "image_display",
        ]

    def get_image_display(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return obj.image_url


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class LogoSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Logo
        fields = ['id', 'logo', 'logo_url', 'alt_text', 'updated_at']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        elif obj.logo:
            return obj.logo.url
        return None


class FeedbackSerializer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = [
            'id',
            'name',
            'message',
            'profile_photo',
            'profile_photo_url',
            'created_at',
            'created_at_formatted'
        ]

    def get_profile_photo_url(self, obj):
        request = self.context.get('request')
        if obj.profile_photo and request:
            return request.build_absolute_uri(obj.profile_photo.url)
        elif obj.profile_photo:
            return obj.profile_photo.url
        return None

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%B %d, %Y at %I:%M %p")
