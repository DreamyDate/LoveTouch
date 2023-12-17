from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat_app import consumers
from notifications import consumers as notification_consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/notifications/', notification_consumers.NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
