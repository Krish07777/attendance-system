"""
Django settings for attendance_system project.
"""

from pathlib import Path
import os   # ✅ IMPORTANT

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = "django-insecure-deh$i_-w-vlfu8x6xvs=up(yytc-$m0zgzpj^a_lr-)ob3k9+i"
DEBUG = True
ALLOWED_HOSTS = ['*']

# INSTALLED APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "students",
]


# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URL CONFIG
ROOT_URLCONF = "attendance_system.urls"


# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # you can add custom template folder later
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


# WSGI
WSGI_APPLICATION = "attendance_system.wsgi.application"


# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ✅ STATIC FILES (🔥 MOST IMPORTANT PART)
STATIC_URL = '/static/'   # FIXED

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'students/static')   # tells Django where your images are
]


# LOGIN REDIRECT
LOGIN_URL = '/'