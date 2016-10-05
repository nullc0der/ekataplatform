import json
import requests

from django.conf import settings


class OneSignal(object):
    def __init__(self, message, player_ids):
        self.message = message
        self.player_ids = player_ids

    def send_message(self):
        header = {"Content-Type": "application/json",
            "Authorization": settings.DJANGO_ONESIGNAL_KEY}

        payload = {
            "app_id": settings.DJANGO_ONESIGNAL_APP_ID,
            "include_player_ids": self.player_ids,
            "contents": {"en": self.message}
        }

        req = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload)
        )
