from .base import *

DEBUG = True

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

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('DJANGO_EMAIL_HOST')
EMAIL_PORT = 25
EMAIL_HOST_USER = get_env_variable('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': get_env_variable('DJANGO_REDIS_HOST') + ':6379',
    },
}

BROKER_URL = 'redis://' + get_env_variable('DJANGO_REDIS_HOST') + ':6379/0'

# Channel's Config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(get_env_variable('DJANGO_REDIS_HOST'), 6379)],
        },
        "ROUTING": "ekatadeveloper.routing.channel_routing",
    },
}

DBBACKUP_STORAGE_OPTIONS = {'location': '/code/ekatabackups'}
