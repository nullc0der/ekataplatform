from channels import route
from groupsystem import consumers


group_notification_routes = [
    route(
        'websocket.connect',
        consumers.group_notification_connect,
        path=r'^/stream/$'
    ),
    route('websocket.disconnect', consumers.group_notification_disconnect)
]
