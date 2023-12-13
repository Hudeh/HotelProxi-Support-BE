from django.urls import re_path as _

from . import views

urlpatterns = [
    _(
        r"^create_chatroom",
        views.CreateChatRoomView.as_view(),
        name="create_chatroom",
    ),
    _(
        r"^(?P<slug>[\w-]+)/messages$",
        views.MessageView.as_view(),
        name="messages",
    ),
    _(
        r"^chatrooms$",
        views.ChatRoomsView.as_view(),
        name="chatrooms",
    ),
    _(
        r"^room/(?P<name>[\w-]+)$",
        views.ChatRoomView.as_view(),
        name="room",
    ),
    _(
        r"^agent-room/(?P<slug>[\w-]+)$",
        views.ChatRoomAgentView.as_view(),
        name="room",
    ),
    _(
        r"^messages/(?P<slug>[\w-]+)$",
        views.MessageView.as_view(),
        name="room",
    ),
]
