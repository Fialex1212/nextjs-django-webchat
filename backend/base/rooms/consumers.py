import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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

    async def receive(self, text_data):
        # Handle invalid JSON or empty message
        try:
            # Attempt to parse the incoming JSON data
            text_data_json = json.loads(text_data)
            
            # Extract message and username from the parsed JSON
            message = text_data_json.get('message', '')
            username = text_data_json.get('username', '')

            # If message or username are empty, return early
            if not message or not username:
                print(f"Invalid message or username received: {text_data}")
                return

            # Send message to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
        
        except json.JSONDecodeError as e:
            # Log the error if the JSON is invalid
            print(f"Error decoding JSON: {e} - Received data: {text_data}")
            return

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
