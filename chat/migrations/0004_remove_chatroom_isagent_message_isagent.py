# Generated by Django 5.0 on 2023-12-08 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_chatroom_agent_name_chatroom_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatroom",
            name="isAgent",
        ),
        migrations.AddField(
            model_name="message",
            name="isAgent",
            field=models.BooleanField(default=False),
        ),
    ]
