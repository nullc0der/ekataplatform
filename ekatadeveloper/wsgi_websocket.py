import os
import gevent
import redis.connection

redis.connectio.socket = gevent.socket

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "ekatadeveloper.settings.production"
)

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

application = uWSGIWebsocketServer()
