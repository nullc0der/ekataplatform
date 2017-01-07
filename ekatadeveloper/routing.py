from channels import include


channel_routing = [
    include(
        'notification.routing.notification_routes',
        path=r'^/notifications'
    ),
    include(
        'messagingsystem.routing.messaging_routes',
        path=r'^/messaging'
    )
]
