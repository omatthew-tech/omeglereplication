from django.shortcuts import render
from .models import ChatRoom, Message

def index(request):
    chat_rooms = ChatRoom.objects.all()
    context = {'chat_rooms': chat_rooms}
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    chat_room = ChatRoom.objects.get(room_name=room_name)
    messages = Message.objects.filter(room=chat_room)
    context = {'chat_room': chat_room, 'messages': messages}
    return render(request, 'chat/room.html', context)

def live_stream(request):
    return render(request, 'chat/live_stream.html')

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data['type']
        payload = data['payload']

        if type == 'offer':
            await self.send(json.dumps({
                'type': 'offer',
                'offer': payload
            }))
        elif type == 'answer':
            await self.send(json.dumps({
                'type': 'answer',
                'answer': payload
            }))
