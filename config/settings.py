"""
Django settings for the Restaurant Website + Management System.

Dev setup uses SQLite (per project spec: 'SQLite can be used during
initial development'). Swapping to PostgreSQL later is just a matter of
changing the DATABASES dict below -- nothing else in the project needs
to change.
"""

import os
from pathlib import Path
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------
SECRET_KEY = "django-insecure-dev-key-change-before-deployment"

<<<<<<< HEAD
DEBUG = True
ALLOWED_HOSTS = ["*"]  # Vercel সহ সব হোস্ট এলাউ করার জন্য '*' রাখা হয়েছে
=======
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']  # tighten this before deployment
>>>>>>> 1d55985 (Configure project for Render deployment with PostgreSQL and Whitenoise)

# ------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "accounts",
    "restaurant",
    "menu",
    "reviews",
    "reservations",
    "tables",
    "orders",
    "customers",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Vercel-এ CSS/JS পাওয়ার জন্য WhiteNoise যোগ করা হলো
    "django.contrib.sessions.middleware.SessionMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "restaurant.context_processors.restaurant_profile",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# ------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# STATIC & MEDIA FILES
# ------------------------------------------------------------------
<<<<<<< HEAD
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Vercel-এ Static files কমপ্রেসড করার জন্য WhiteNoise Storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
=======
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # used by `collectstatic` in production
>>>>>>> 1d55985 (Configure project for Render deployment with PostgreSQL and Whitenoise)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------
# AUTH REDIRECTS
# ------------------------------------------------------------------
LOGIN_URL = "dashboard_login"
LOGIN_REDIRECT_URL = "dashboard_home"
LOGOUT_REDIRECT_URL = "landing"

# ------------------------------------------------------------------
# MESSAGES
# ------------------------------------------------------------------
from django.contrib.messages import constants as message_constants  # noqa: E402

MESSAGE_TAGS = {
    message_constants.ERROR: "danger",
}