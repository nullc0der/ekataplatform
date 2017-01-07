from channels import route
from notification import consumers


notification_routes = [
    route(
        'websocket.connect',
        consumers.notification_connect,
        path=r'^/stream/$'
    ),
    route('websocket.disconnect', consumers.notification_disconnect)
]
