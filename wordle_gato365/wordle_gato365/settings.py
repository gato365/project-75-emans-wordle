"""
Django settings for wordle_gato365 project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import pytz
from datetime import datetime, time
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add these to your settings.py
WORDLE_TIMEZONE = pytz.timezone('America/Los_Angeles')
WORDLE_RESET_TIME = time(hour=0, minute=0, second=0)


load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6g9e3!e_&!vif@5i^hktv^+lq-y&-=xv-^brjcakq8-f-if4qu'




# SECURITY WARNING: don't run with debug turned on in production!
## 1a) Currently commented out
DEBUG = False


## 1b) Currently in use
# DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['wordle-app-2024-4c250a9e97a3.herokuapp.com', 'localhost', '127.0.0.1','www.thewurdz.org','thewurdz.org']
CSRF_TRUSTED_ORIGINS = ['https://www.thewurdz.org']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


## Custom user model
AUTH_USER_MODEL = 'users.CustomUser'




# Application definition

INSTALLED_APPS = [
    'wordle.apps.WordleConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'crispy_forms',
    'crispy_bootstrap4',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'wordle_gato365.no_cache_middleware.NoCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'allauth.account.middleware.AccountMiddleware',
    # 'django_db_geventpool.middleware.GeventPoolMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wordle_gato365.urls'


## TEMPLATES settings for Django 3.2
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # This line is crucial
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

## WSGI application for deployment
WSGI_APPLICATION = 'wordle_gato365.wsgi.application'


## Authentication settings for allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1





# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Check if the environment variable 'DATABASE_URL' is set
if os.getenv('DATABASE_URL'):
    # Use the remote database configuration
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
else:
    # Use the local database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'your_default_db_name'),
            'USER': os.getenv('DB_USER', 'your_default_db_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'your_default_db_password'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'CONN_MAX_AGE': 0,
            'POOL_SIZE': 5,  # Adjust pool size as needed
            'MAX_OVERFLOW': 10  # Adjust max overflow as need
              
        }
    }






# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True




# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # For development, you might want to use the default storage
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'wordle', 'static'),
]


## --------- All added by me ---------------

## Custom settings for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/profile_pics')
MEDIA_URL = '/media/profile_pics/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'


LOGIN_REDIRECT_URL = '/game-history/'
LOGIN_URL = '/game-history/'





# Set the time zone
TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True

# Define the reset time (midnight PST)
WORDLE_RESET_TIME = time(hour=0, minute=0, second=0)


## Logging settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'wordle': {  # replace with your app name
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
