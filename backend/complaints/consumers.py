import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Complaint
from django.contrib.auth import get_user_model

class ComplaintChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.complaint_id = self.scope['url_route']['kwargs']['complaint_id']
        self.room_group_name = f'chat_{self.complaint_id}'

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
        user_id = self.scope["user"].id

        # Save to DB
        await self.save_message(user_id, self.complaint_id, message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

    @database_sync_to_async
    def save_message(self, user_id, complaint_id, content):
        from .models import ChatMessage, Complaint
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            user = get_user_model().objects.get(id=user_id)
            ChatMessage.objects.create(complaint=complaint, sender=user, content=content)
        except Exception:
            pass

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id
        }))
