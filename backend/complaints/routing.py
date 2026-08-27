from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<complaint_id>\w+)/$', consumers.ComplaintChatConsumer.as_asgi()),
]
