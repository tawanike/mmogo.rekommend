import os
import socket
from datetime import timedelta
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration, TRANSACTION_STYLE_VALUES
from sentry_sdk.integrations.celery import CeleryIntegration

load_dotenv()
sentry_sdk.init(
    dsn="https://fb710debf28a4a37acebc78ab7a2a6a0@o396687.ingest.sentry.io/5253053",
    integrations=[DjangoIntegration(), CeleryIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

HOST = socket.gethostname()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APPEND_SLASH = False
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'https://42f52e71.ngrok.io']
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'https://42f52e71.ngrok.io']

HOST = socket.gethostname()
# Application definition

INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'storages',

    'altur.sms',
    'altur.push',
    'altur.email',

    
    'commace.stores',
    'commace.products',
    'commace.payments',
    'commace.contrib.cart',
    'commace.contrib.brands',
    'commace.contrib.promocodes',
    'commace.contrib.shoppinglists',
    

    'mmogo.profiles',
    'mmogo.contrib.links',
    'mmogo.contrib.devices',
    'mmogo.contrib.events',
    'mmogo.contrib.banners',
    'mmogo.contrib.addresses',
    'mmogo.contrib.locations',
    'mmogo.contrib.activities',
    'mmogo.contrib.categories',
    'mmogo.contrib.invitations',
    'mmogo.contrib.medialibrary',
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
]

ROOT_URLCONF = 'admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'admin.wsgi.application'
ASGI_APPLICATION = 'admin.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv('SQL_DATABASE_ENGINE'),
        "NAME": os.getenv('SQL_DATABASE_NAME'),
        "USER": os.getenv('SQL_DATABASE_USER'),
        "PASSWORD": os.getenv('SQL_DATABASE_PASSWORD'),
        "HOST": os.getenv('SQL_DATABASE_HOST'),
        "PORT": os.getenv('SQL_DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'api/public'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

# CELERY STUFF
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Johannesburg'
BROKER_URL = f'sqs://{AWS_ACCESS_KEY_ID}:{AWS_SECRET_ACCESS_KEY}@sqs.af-south-1.amazonaws.com/677760231496/celery'

BROKER_TRANSPORT_OPTIONS = {'region': AWS_DEFAULT_REGION}

INTERNAL_IPS = [
    '127.0.0.1',
]
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}



# This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.'+ AWS_DEFAULT_REGION +'.amazonaws.com'

# static media settings
STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.'+ AWS_DEFAULT_REGION +'.amazonaws.com/'
MEDIA_URL = 'media/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

STATIC_ROOT = 'staticfiles'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_DEFAULT_ACL = "public-read"
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

CLOUDFRONT_DOMAIN = ''
CLOUDFRONT_ID = ''

# AWS_QUERYSTRING_AUTH = False
# AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN
# AWS_CLOUDFRONT_DOMAIN = 'd1wzpxdhx5pce6.cloudfront.net/'

TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
TWILIO_AUTH_TOKEN = os.environ.get("AWS_STORAGE_BUCKET_NAME")
TWILIO_ACCOUNT_SID = os.environ.get("AWS_STORAGE_BUCKET_NAME")

CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_INVOICE_TEMPLATE_ID = 'd-06dac412a1914937b4a742fe263be834'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_API_KEY")

EMAIL_PORT = 587
EMAIL_USE_TLS = True

REQUIRE_MOBILE = False

POSTMAN = 'thuli@wddng.co'
DOMAIN = os.getenv('DOMAIN')
SITE_NAME = os.getenv('SITE_NAME')

DOMAIN = os.getenv('DOMAIN')
SITE_NAME = os.getenv('SITE_NAME')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

PUSH_NOTIFICATION_SERVICE = 'expo'
EXPO_ACCESS_TOKEN = os.getenv('EXPO_ACCESS_TOKEN')

SLACK_WEBHOOK = ''
SERVICE_FEE = 45.00

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



try:
    from .local_settings import *
except ImportError:
    pass
