import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PortfolioChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "Connected to chat!"}))

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        query = text_data_json.get("query", "")
        portfolio_id = text_data_json.get("portfolio_id")

        if not portfolio_id:
            await self.send_error("Missing portfolio_id")
            return

        if not query:
            await self.send_error("Empty query")
            return

        response = f"AI response for portfolio {portfolio_id}: {query}"

        await self.send(text_data=json.dumps({"response": response}))

    async def send_error(self, error_message):
        await self.send(json.dumps({"error": error_message}))
