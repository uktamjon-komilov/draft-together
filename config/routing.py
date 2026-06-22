from django.urls import path

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EchoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({"message": f"Hello {self.scope["user"]}"})

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    async def disconnect(self, close_code):
        pass


websocket_urlpatterns = [
    path("echo/", EchoConsumer.as_asgi()),
]
