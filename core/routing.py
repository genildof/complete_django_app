from django.conf.urls import url

from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from core.consumers import core_WebSocketConsumer

# Consumer Imports


application = ProtocolTypeRouter({

    # WebSocket handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/$", core_WebSocketConsumer.as_asgi()),
        ])
    ),
    "channel": ChannelNameRouter({
    
    })
})
