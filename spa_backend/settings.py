from pathlib import Path
from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # ✅ ADDED

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-ofu^dh3eyk5*nx9fz(^-d4u)0@gv6)h5w@s9v1&7+c19(5f60)'

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "https://spa-project-frontend.onrender.com"
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

CORS_ALLOW_ALL_ORIGINS = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'spa_backend.urls'

ALLOWED_HOSTS = ['*']


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'spa_backend.wsgi.application'


# ================= DATABASE FIX =================

# ✅ USE PostgreSQL if DATABASE_URL exists
# ✅ Otherwise fallback to your SQLite (no data loss locally)

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=True
    )
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'


ADMIN_CSS = {
    'all': ('admin/css/custom_admin.css',),
}


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


WHATSAPP_ACCESS_TOKEN = "EAAUeSsyBHFABQq8G5WoGRiRNfts1m7JZA5wwOQWJoodrMJEs3V5mx2rRRI5sT2r2p9iNq4PJhBgnjp53kEBSmaAx6ZAPjAG6r46fwo1zmM5czgHsDWQt6pZCO17z4BToeYPiZAXqcEoI2YKA1DWFh5hw80ZAC4xn3ZAnkOIoz3wNR7BxqqYf8hVr7ssRBwJEbdtD3gLvLO78U0T6CNNoDFBBuUexCbDoRZCjs9sZBQ9aSWthUIT5ZCVFApxlLHQGLE7wQuALrfBsCKLG3p3NJKgZAV"
WHATSAPP_PHONE_NUMBER_ID = "960822447113982"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


INSTALLED_APPS += [
    'rest_framework_simplejwt.token_blacklist',
]


SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


ADMIN_SITE_HEADER = "Elegant Thai Spa - Admin Dashboard"
ADMIN_SITE_TITLE = "Elegant Thai Spa Admin"
ADMIN_INDEX_TITLE = "Welcome to Elegant Thai Spa Administration"


ADMIN_CSS = {
    'all': ('admin/css/custom_admin.css',),
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'elegantthais@gmail.com'
EMAIL_HOST_PASSWORD = 'ncyo qyeo nfdn rxzz'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = 'elegantthais@gmail.com'


RAZORPAY_KEY_ID = "rzp_test_S12kgos03uuacA"
RAZORPAY_KEY_SECRET = "jvRifBb3bYscwP5onsQyZ4BT"
