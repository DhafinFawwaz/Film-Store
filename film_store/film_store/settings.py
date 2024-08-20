"""
Django settings for film_store project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta # used for JWT token expiration
from dotenv import load_dotenv
import os
import platform

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!6hg7mwm+-f%xs477^ic73yndqzj6%kk6n&iu_*7hf=^hh6l9j'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
true_str = os.environ.get('DEBUG', False)
DEBUG = true_str == True or true_str == 'True' or true_str == 'true'

ALLOWED_HOSTS = [
    "filmstore-gokbzfw6.b4a.run",
    "127.0.0.1",
    "192.168.100.6",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_cleanup.apps.CleanupConfig', # Automatically delete media files when update or delete
    'tailwind',
    'theme',
    'django_browser_reload',
    'drf_yasg'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'film_store.urls'


STATICFILES_DIRS = [
    BASE_DIR / "theme" / "static",
    BASE_DIR / "templates",
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': STATICFILES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'film_store.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# supabase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PORT': os.environ.get('DB_PORT'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'NAME': 'app.validator.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'COERCE_DECIMAL_TO_STRING': False, # Change DecimalField to json number instead of string
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
     ),
     'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    "SIGNING_KEY": SECRET_KEY,
}

CORS_ALLOWED_ORIGINS = [
    "https://labpro-fe.hmif.dev",
    "http://localhost:8000",
    "http://localhost:5173",
    "http://127.0.0.1:8000"
]

AUTH_USER_MODEL = 'app.GeneralUser'

SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies" # Use HttpOnly cookie as said in specification


# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]


NPM_BIN_PATH = '/usr/bin/npm'
if platform.system() == "Linux":
    NPM_BIN_PATH = '/usr/bin/npm'
else:
    NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"


CSRF_TRUSTED_ORIGINS = [
    "https://filmstore-gokbzfw6.b4a.run",
    "http://127.0.0.1:8000",
    "https://labpro-fe.hmif.dev/"
]

if os.environ.get('USE_SUPABASE'):
    DEFAULT_FILE_STORAGE = 'film_store.storage.SupabaseStorage'
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_ROOT_PATH = '/'


DATASET_URL = os.environ.get('DATASET_URL')

# API Documentation
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
   }
}


# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_HOST'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

USE_X_FORWARDED_HOST = True