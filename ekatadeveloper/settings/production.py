from .base import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DEBUG = False

ALLOWED_HOSTS = ['beta.ekata.social', 'ekata.social']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DJANGO_DATABASE_NAME'),
        'USER': get_env_variable('DJANGO_DATABASE_USERNAME'),
        'PASSWORD': get_env_variable('DJANGO_DATABASE_PASSWORD'),
        'HOST': get_env_variable('DJANGO_DATABASE_HOST'),
        'PORT': '',
    }
}

STATIC_URL = '/statics/'

STATIC_ROOT = os.path.join(BASE_DIR, "statics")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('DJANGO_EMAIL_HOST')
EMAIL_PORT = 25
EMAIL_HOST_USER = get_env_variable('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_TOKEN_SECURE = True

X_FRAME_OPTIONS = 'DENY'

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': get_env_variable('DJANGO_REDIS_HOST') + ':6379',
    },
}

BROKER_URL = 'redis://' + get_env_variable('DJANGO_REDIS_HOST') + ':6379/0'
