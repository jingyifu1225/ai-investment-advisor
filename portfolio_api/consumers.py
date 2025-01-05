import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PortfolioChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        query = text_data_json.get("query", "")
        portfolio_id = text_data_json.get("portfolio_id")

        # Here you would integrate with your AI service
        response = f"AI response for portfolio {portfolio_id}: {query}"

        await self.send(text_data=json.dumps({"response": response}))
