from __future__ import absolute_import, unicode_literals

import os
import ssl
from django.conf import settings
from decouple import config
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery(
    "core",
    broker=config("REDIS_URL"),
    backend=config("REDIS_URL"),
    redbeat_redis_url=config("REDIS_URL")
)

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
