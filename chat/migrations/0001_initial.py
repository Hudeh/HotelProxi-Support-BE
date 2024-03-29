# Generated by Django 5.0 on 2024-01-28 14:51

import chat.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("agent_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "Waiting"),
                            ("active", "Active"),
                            ("closed", "Closed"),
                        ],
                        default="waiting",
                        max_length=20,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("slug", models.SlugField(unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                "ordering": ("-created_at",),
                "permissions": [
                    ("custom_chat_room_delete", "Can delete chat room"),
                    ("custom_chat_room_add", "Can add chat room"),
                    ("custom_chat_room_view", "Can view chat room"),
                    ("custom_chat_room_edit", "Can edit chat room"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sender", models.CharField(max_length=255)),
                ("message", models.TextField(blank=True, null=True)),
                ("is_agent", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "attachment",
                    models.FileField(
                        blank=True, null=True, upload_to=chat.models.get_upload_path
                    ),
                ),
                (
                    "chat_room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chatroom"
                    ),
                ),
            ],
            options={
                "ordering": ("timestamp",),
            },
        ),
    ]
