from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


from django.db import models

class Service(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Image options
    image = models.ImageField(upload_to="services/", null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# NEW MODEL for different price & duration options
class ServiceOption(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='options')
    
    duration = models.IntegerField()  # in minutes
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.service.name} - {self.duration} mins - ₹{self.price}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("PAY_AT_SERVICE", "Pay at Service"),
        ("ONLINE", "Online Payment"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    customer_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    # 🔥 PAYMENT FIELDS (NEW)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="PAY_AT_SERVICE"
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()

    image = models.ImageField(upload_to="about/", blank=True, null=True)
    unsplash_url = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    TYPE_CHOICES = [
        ("contact", "Contact Us"),
        ("bug", "Report Bug"),
        ("chatbot", "Chatbot AI"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.upper()} - {self.email}"

class AdminContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return "Admin Contact Info"

class Location(models.Model):
    title = models.CharField(max_length=150, default="Visit Us")
    address = models.TextField(default="K-5, Kalinga Vihar LIG, Kalinganagar, Bhubaneswar, Odisha – 751028")
    opening_days = models.CharField(max_length=100, default="Monday – Sunday")
    opening_time = models.CharField(max_length=50, default="10:00 AM")
    closing_time = models.CharField(max_length=50, default="9:00 PM")
    map_query = models.CharField(
        max_length=500,
        default="K-5, Kalinga Vihar LIG, Kalinganagar, Bhubaneswar, Odisha 751028",
        help_text="Address, coordinates, or place ID used for map embedding and directions."
    )
    map_embed_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional: direct Google Maps link (e.g., https://maps.app.goo.gl/...) — takes precedence over map_query."
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Location Info"

from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Logo(models.Model):
    logo = models.ImageField(upload_to='logos/')
    alt_text = models.CharField(max_length=100, default='Elegant Thai Spa Logo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Spa Logo"

    class Meta:
        verbose_name_plural = "Logo"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    profile_photo = models.ImageField(upload_to='feedback/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"

    class Meta:
        ordering = ['-created_at']