# chat/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    ]),
})

# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    type = text_data_json['type']
    sender_id = text_data_json['sender_id']
    receiver_id = text_data_json['receiver_id']

    # Send message to room group
    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }
    )

