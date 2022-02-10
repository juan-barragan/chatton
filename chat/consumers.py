import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # wait for joining room, channel_layer commes from redis channels
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # this comes from JavaScript on the room.html page
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        await self.save_message(username, room, message)
        # Broadcast
        await self.channel_layer.group_send(self.room_group_name, { 'type': 'chat_message', 'message': message, 'username': username })

    async def chat_message(self, event):
        message = event['message'] 
        username = event['username']

        await self.send(text_data = json.dumps({'message': message, 'username': username }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)