from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ================= SECURITY =================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-default-key")
DEBUG = False

ALLOWED_HOSTS = [
    "spa-project-backend-1.onrender.com",
    "spa-project-frontend.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://spa-project-frontend.onrender.com",
    "https://spa-project-backend-1.onrender.com",
]

# ================= APPS =================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
    "rest_framework_simplejwt.token_blacklist",
]

# ================= CORS =================

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://spa-project-frontend.onrender.com",
]
CORS_ALLOW_CREDENTIALS = True

# ================= MIDDLEWARE =================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spa_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spa_backend.wsgi.application"

# ================= DATABASE =================

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# ================= REST =================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# ================= PASSWORDS =================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ================= INTERNATIONALIZATION =================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ================= STATIC =================

STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ================= MEDIA =================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# In production, serve media via backend domain
if not DEBUG:
    MEDIA_URL = "https://spa-project-backend-1.onrender.com/media/"

# ================= JWT =================

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ================= ADMIN =================

ADMIN_SITE_HEADER = "Elegant Thai Spa - Admin Dashboard"
ADMIN_SITE_TITLE = "Elegant Thai Spa Admin"
ADMIN_INDEX_TITLE = "Welcome to Elegant Thai Spa Administration"

ADMIN_CSS = {"all": ("admin/css/custom_admin.css",)}

# ================= EMAIL =================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", EMAIL_HOST_USER)

# ================= WHATSAPP =================

WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

# ================= RAZORPAY =================

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
