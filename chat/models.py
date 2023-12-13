import os
from django.db import models
from django.conf import settings


def get_upload_path(instance, filename):
    # Determine the upload path based on the file type
    if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
        return os.path.join("media", "picture", filename)
    elif filename.endswith((".mp4", ".avi", ".mov")):
        return os.path.join("media", "video", filename)
    else:
        return os.path.join("media", "other", filename)


class ChatRoom(models.Model):
    WAITING = "waiting"
    ACTIVE = "active"
    CLOSED = "closed"

    CHOICES_STATUS = (
        (WAITING, "Waiting"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed"),
    )

    name = models.CharField(max_length=255)
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        permissions = [
            ("custom_chat_room_delete", "Can delete chat room"),
            ("custom_chat_room_add", "Can add chat room"),
            ("custom_chat_room_view", "Can view chat room"),
            ("custom_chat_room_edit", "Can edit chat room"),
        ]

        ordering = ("-created_at",)


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    is_agent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.sender

    class Meta:
        ordering = ("timestamp",)
