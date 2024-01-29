import json
import base64
from django.utils.timesince import timesince
from django.core.files.base import ContentFile
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions.StopConsumer import StopConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message
from user.models import ChatUser


def initials(value):
    initials = ""

    for name in value.split(" "):
        if name and len(initials) < 3:
            initials += name[0].upper()

    return initials


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.set_room_active()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        raise StopConsumer()

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get("type")
        attachment = data.get("attachment")
        message = data.get("message")
        sender = data.get("sender")
        chat_room = data.get("chat_room")
        is_agent = data.get("is_agent")
        fileType = None
        if type == "message":
            new_message = await self.save_message(
                sender, chat_room, message, is_agent, attachment
            )
            file_url = new_message.attachment.url if new_message.attachment else None
            if file_url is not None:
                if (
                    ".mp4" in file_url.lower()
                    or ".avi" in file_url.lower()
                    or ".mov" in file_url.lower()
                ):
                    fileType = "video"

                elif (
                    ".jpg" in file_url.lower()
                    or ".jpeg" in file_url.lower()
                    or ".png" in file_url.lower()
                    or ".gif" in file_url.lower()
                ):
                    fileType = "image"
                else:
                    fileType = "file"
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                    "attachment": file_url,
                    "fileType": fileType,
                    "is_agent": is_agent,
                    "initials": initials(sender),
                    "timestamp": timesince(new_message.timestamp),
                },
            )
        elif type == "update":
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "writing_active",
                    "message": message,
                    "sender": sender,
                    "initials": initials(sender),
                    "is_agent": is_agent,
                },
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        attachment = event["attachment"]
        initials = event["initials"]
        timestamp = event["timestamp"]
        type = event["type"]
        is_agent = event["is_agent"]
        fileType = event["fileType"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": sender,
                    "attachment": attachment,
                    "fileType": fileType,
                    "timestamp": timestamp,
                    "initials": initials,
                    "type": type,
                    "is_agent": is_agent,
                }
            )
        )

    async def writing_active(self, event):
        # Send writing is active to room
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "is_agent": event["is_agent"],
                    "message": event["message"],
                    "sender": event["sender"],
                    "initials": event["initials"],
                }
            )
        )

    async def users_update(self, event):
        # Send information to the web socket (front end)
        await self.send(text_data=json.dumps({"type": "users_update"}))

    # get room
    @sync_to_async
    def get_room(self):
        self.room = ChatRoom.objects.get(slug=self.room_name)

    @sync_to_async
    def set_room_closed(self):
        self.room = ChatRoom.objects.get(slug=self.room_name)
        self.room.status = ChatRoom.CLOSED
        self.room.save()

    @sync_to_async
    def set_room_active(self):
        self.room = ChatRoom.objects.get(slug=self.room_name)
        self.room.status = ChatRoom.ACTIVE
        self.room.save()

    @sync_to_async
    def save_message(self, sender, chat_room, message, is_agent, attachment):
        room = ChatRoom.objects.get(slug=chat_room)

        msg = Message.objects.create(
            sender=sender, chat_room=room, message=message, is_agent=is_agent
        )
        try:
            if attachment:
                ext = attachment.split(",")[0].split("/")[1].split(";")[0]
                file_content = base64.b64decode(attachment.split(",")[1])
                file_content_file = ContentFile(file_content)
                msg.attachment.save(
                    f"chat_file.{ext}",
                    file_content_file,
                    save=True,
                )
            return msg
        except:
            pass
