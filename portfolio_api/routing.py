from django.urls import re_path
import consumers

websocket_urlpatterns = [
    re_path(r"ws/portfolio/chat/$", consumers.PortfolioChatConsumer.as_asgi()),
]
