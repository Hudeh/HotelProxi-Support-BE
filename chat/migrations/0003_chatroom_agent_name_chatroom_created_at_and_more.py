# Generated by Django 5.0 on 2023-12-08 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="agent_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="isAgent",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="status",
            field=models.CharField(
                choices=[
                    ("waiting", "Waiting"),
                    ("active", "Active"),
                    ("closed", "Closed"),
                ],
                default="waiting",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.CharField(max_length=255),
        ),
    ]
