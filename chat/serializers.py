# serializers.py

from rest_framework import serializers
from .models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = "__all__"


class ChatRoomPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ["name","is_active"]
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"
