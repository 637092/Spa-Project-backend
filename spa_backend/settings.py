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
# Removed STATICFILES_DIRS since you don’t have a static/ folder

# ================= MEDIA =================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Do not override MEDIA_URL in production — use cloud storage later

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

EMAIL_HOST_USER = os.environ.get("elegantthais@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("ncyo qyeo nfdn rxzz")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = EMAIL_HOST_USER

# ================= WHATSAPP =================

WHATSAPP_ACCESS_TOKEN = os.environ.get("EAAUeSsyBHFABQq8G5WoGRiRNfts1m7JZA5wwOQWJoodrMJEs3V5mx2rRRI5sT2r2p9iNq4PJhBgnjp53kEBSmaAx6ZAPjAG6r46fwo1zmM5czgHsDWQt6pZCO17z4BToeYPiZAXqcEoI2YKA1DWFh5hw80ZAC4xn3ZAnkOIoz3wNR7BxqqYf8hVr7ssRBwJEbdtD3gLvLO78U0T6CNNoDFBBuUexCbDoRZCjs9sZBQ9aSWthUIT5ZCVFApxlLHQGLE7wQuALrfBsCKLG3p3NJKgZAV")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("960822447113982")

# ================= RAZORPAY =================

RAZORPAY_KEY_ID = os.environ.get("rzp_test_S12kgos03uuacA")
RAZORPAY_KEY_SECRET = os.environ.get("jvRifBb3bYscwP5onsQyZ4BT") 
