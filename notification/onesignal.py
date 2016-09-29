import json
import requests


class OneSignal(object):
    def __init__(self, message, player_ids):
        self.message = message
        self.player_ids = player_ids

    def send_message(self):
        header = {"Content-Type": "application/json",
            "Authorization": "Basic YTBlYjVhYjMtYjZmZC00Njg3LTg4NDItMTFlNDZiZGU3ZmMw"}

        payload = {
            "app_id": "69dc9060-3af3-4209-82c7-7de5219830b3",
            "include_player_ids": self.player_ids,
            "contents": {"en": self.message}
        }

        req = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload)
        )
