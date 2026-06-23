from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from rooms.models import Room


@database_sync_to_async
def get_room(_id):
    try:
        return Room.objects.get(id=_id)
    except Room.DoesNotExist:
        return None


class WhiteboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.accept()
            return await self.close(code=4001)

        room_id = self.scope["url_route"]["kwargs"].get("room_id")

        room = await get_room(room_id)

        if room is None:
            await self.accept()
            return await self.close(code=4004)

        self.room_group = f"room_{room_id}"
        await self.channel_layer.group_add(self.room_group, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, "room_group"):
            await self.channel_layer.group_discard(self.room_group, self.channel_name)
        return await super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "room.message",
                "payload": content,
            },
        )

    async def room_message(self, event):
        await self.send_json(event["payload"])