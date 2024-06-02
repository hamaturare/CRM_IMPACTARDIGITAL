from pathlib import Path
import os
from decouple import Config, RepositoryEnv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to the .env file
env_path = BASE_DIR / '.env'
config = Config(RepositoryEnv(str(env_path)))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-+=k9m(bcfnr*o-j&zy0+17*zt%0a$01+z9(feyce3jh-!vf1zp')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['fmendes.pythonanywhere.com', '127.0.0.1']


# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'django_cleanup',
    'nested_admin',

]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOCAL_APPS = [
    'apps.common',
    'apps.userprofile',
    'apps.leads',
    'apps.clients',
    'apps.ideabox',
    'apps.wpmessages',

]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CRM_ID.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',],
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

WSGI_APPLICATION = 'CRM_ID.wsgi.application'


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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

try:
    from CRM_ID.local_settings import *
except ImportError:
    pass

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# This will print email in Console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'crm.impactardigital.com.br'
#EMAIL_PORT = 465
#EMAIL_USE_TLS = False
#MAIL_USE_SSL = True
#EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
#DEFAULT_FROM_EMAIL = 'noreplyt@crm.impactardigital.com.br'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

WHATSAPP_API_URL = 'https://graph.facebook.com/v19.0/352309607958630/messages'
WHATSAPP_ACCESS_TOKEN = 'Bearer EAATatv2lO34BOzl7ggqPhsOE0iVOAG7c1JudTxGXQpX7FZBfhmO0YfoHCUTA7hLu4efDEMlQi0aTmmKN5bEQs1fFy7tfeCr81J7fzubfgOTlEUhsNE6Y67W4ZA3M9f5jMocRWClAetvjlKvJP7n06qwYPXgDBmBB1KyLWSCh7DByoD17jzMs9ResAzlw6ab6yvXaYm2Y96RnK2I7YZCBb6twXPu5ZAWt8PcZD'
WHATSAPP_VERIFY_TOKEN = 'e4679551-2c1e-420a-92a0-40d965a8a66f'

#WHATSAPP_PHONE_ID = config('WHATSAPP_PHONE_ID')
#WHATSAPP_VERIFY_TOKEN = config('WHATSAPP_VERIFY_TOKEN')

#SECURE_SSL_REDIRECT = True
