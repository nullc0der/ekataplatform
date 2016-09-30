"""
Django settings for ekatadeveloper project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import raven
import django.conf.locale
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'django_forms_bootstrap',
    'ws4redis',
    'bootstrap_pagination',
    'versatileimagefield',
    'phonenumber_field',
    'guardian',
    'markdownx',
    'markdown_deux',
    'raven.contrib.django.raven_compat',
    'landing',
    'profilesystem',
    'publicusers',
    'dashboard',
    'useraccount',
    'information',
    'usertimeline',
    'notification',
    'messagingsystem',
    'hashtag',
    'groupsystem',
    'invitationsystem'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'profilesystem.middleware.CheckInvitationMiddleware',
    'profilesystem.middleware.RemoveSkippedMiddleware'
]

ROOT_URLCONF = 'ekatadeveloper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.core.context_processors.static',
                'ws4redis.context_processors.default',
            ],
        },
    },
]

WSGI_APPLICATION = 'ws4redis.django_runserver.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Authentication

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = "/dashboard/"
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
SOCIALACCOUNT_ADAPTER = 'profilesystem.adapter.SocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'email',
            'public_profile',
            'user_friends',
            'publish_actions',
            'user_photos'
        ],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'gender',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'
    },
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

    # Per object permission
    'guardian.backends.ObjectPermissionBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('as', _('Assamese')),
]

EXTRA_LANG_INFO = {
    'as': {
        'code': 'as',
        'name': 'assamese',
        'name_local': u'\u0985\u09b8\u09ae\u09c0\u09af\u09bc\u09be',
    }
}

LANG_INFO = dict(django.conf.locale.LANG_INFO.items() + EXTRA_LANG_INFO.items())
django.conf.locale.LANG_INFO = LANG_INFO

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

# Number of seconds that we will keep track of inactive users before
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7

# Number of seconds a user's online status will be in cache
USER_ONLINE_TIMEOUT = 25


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SITE_ID = 1

# Celery
BROKER_URL = 'redis://localhost:6379/0'


# Websocket
WEBSOCKET_URL = '/ws/'
WS4REDIS_PREFIX = 'ws'
WS4REDIS_HEARTBEAT = '--heartbeat--'
WS4REDIS_EXPIRE = 5


# Per object permission - Guardian
GUARDIAN_RENDER_403 = True

# Bleach sanitize
BLEACH_VALID_TAGS = ['p', 'b', 'i', 'u',
                     'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                     'strike', 'ul', 'li', 'ol', 'br',
                     'span', 'blockquote', 'hr', 'a', 'img']
BLEACH_VALID_ATTRS = {
    'span': ['style', 'class'],
    'p': ['align', ],
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'style'],
}
BLEACH_VALID_STYLES = ['color', 'cursor', 'float', 'margin']

RAVEN_CONFIG = {
    'dsn': 'https://547e121cbafa4461957d0bae06509cad:48afe776b910408f8f732389ac26f696@sentry.io/101555',
    'release': raven.fetch_git_sha(BASE_DIR),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
