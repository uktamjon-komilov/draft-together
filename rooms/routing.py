from django.urls import path

from .consumers import WhiteboardConsumer


websocket_urlpatterns = [
    path("rooms/<room_id>/", WhiteboardConsumer.as_asgi()),
]
