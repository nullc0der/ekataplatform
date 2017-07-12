from __future__ import unicode_literals

from django.apps import AppConfig


class UseractivityConfig(AppConfig):
    name = 'useractivity'

    def ready(self):
        import useractivity.signals
