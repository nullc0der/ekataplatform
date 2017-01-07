import os
from channels.asgi import get_channel_layer

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ekatadeveloper.settings")

channel_layer = Sentry(get_channel_layer())
