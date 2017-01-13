from channels import route
from messagingsystem import consumers


messaging_routes = [
    route(
        'websocket.connect',
        consumers.messaging_connect,
        path=r'^/stream/$'
    ),
    route('websocket.disconnect', consumers.messaging_disconnect)
]
