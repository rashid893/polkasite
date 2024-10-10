"""
Django settings for polka project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9tl6t!#j945@khg%q6-dy*6_6#%-n_k#2#a%7o)rz=0hlw&cy9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['91.235.116.250','api.bittensorstaking.com','172.17.0.1'] #shaukat
# ALLOWED_HOSTS = ['127.0.0.1','85.239.241.96']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    'corsheaders',
    'django_crontab',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
#    'corsheaders.middleware.CorsMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
   "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "polka.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "polka.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CSRF_TRUSTED_ORIGINS = ['https://*.bittensorstaking.com']


#CORS_ALLOWED_ORIGINS = ['http://91.235.116.250', 'http://imp22']  # shaukat


#CSRF_TRUSTED_ORIGINS = ['http://91.235.116.250:8001']

CSRF_TRUSTED_ORIGINS = [
    'https://api.bittensorstaking.com',
    'https://bittensorstaking.com',
]

# # Schedule the Celery task
CELERY_BEAT_SCHEDULE = {
    'fetch-data-task': {
        'task': 'core.views.fetch_and_save_data',
        'schedule': 300,  # Run the task every 5 minutes (300 seconds)
    },
    'fetch-data-tasks': {
        'task': 'core.views.scripts',
        'schedule': 86400,  # Run the task every 3600 seconds (3600 seconds)
    },
    #     #calculate_and_save_apr_every_two_hours
    # 'calculate_and_save_apr_every_two_hours': {
    #     'task': 'core.views.calculate_and_save_apr_every_two_hours',
    #     'schedule': 300,  # Run the in once every week
    # },
    'calculate_and_save_average': {
        'task': 'core.views.calculate_and_save_average',
        'schedule': 21600,  # Run the in once every week
    },

      
}

# settings.py
BROKER_URL = 'pyamqp://root:GU%23S84_9du%24hg%40f%25Gewj@127.0.0.1:5672//'

# Example RabbitMQ configuration
#BROKER_URL = 'pyamqp://root:GU#S84_9du$hg@f%Gewj@127.0.0.1:5672//' # shaukat
# BROKER_URL = 'pyamqp://pdf:shamlat42wx@127.0.0.1:5672//'
CELERY_RESULT_BACKEND = 'rpc://'
# Celery settings
# Task acknowledgment and prefetch settings
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Broker transport options

#CELERY_RESULT_BACKEND = 'django-db'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

# CRONJOBS = [
#     ('*/5 * * * *', 'core.views.fetch_and_save_data', '> ./file.log')
# ]
#CSRF_TRUSTED_ORIGINS=['https://*.api.bittensorstaking.com/']
#CSRF_TRUSTED_ORIGINS = ['https://api.bittensorstaking.com']

#CORS_ALLOWED_ORIGINS = [
 #   "https://bittensorstaking.com",
#]

CORS_ALLOWED_ORIGINS = ['http://91.235.116.250', 'http://imp22','https://bittensor-staking.vercel.app',"https://api.bittensorstaking.com","https://bittensorstaking.com"] #shaukat
# CORS_ALLOWED_ORIGINS = ['http://127.0.0.1','https://bittensor-staking.vercel.app']

CSRF_TRUSTED_ORIGINS = ['http://91.235.116.250:8001','https://*.api.bittensorstaking.com/'] #shaukat
# CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','https://bittensor-staking.vercel.app','https://85.239.241.96']

#STATICFILES_DIRS=[
 #   os.path.join(BASE_DIR,'static')
#]
#CORS_ALLOW_ALL_ORIGINS =True

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
APPEND_SLASH = True

