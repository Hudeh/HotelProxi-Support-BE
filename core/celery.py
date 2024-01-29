from __future__ import absolute_import, unicode_literals

import os
import ssl
from django.conf import settings
from decouple import config
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery(
    "core",
    broker=config(
        "redis://redis-cluster.alsn3y.ng.0001.euw2.cache.amazonaws.com:6379/0"
    ),
    backend=config(
        "redis://redis-cluster.alsn3y.ng.0001.euw2.cache.amazonaws.com:6379/0"
    ),
    redbeat_redis_url=config(
        "redis://redis-cluster.alsn3y.ng.0001.euw2.cache.amazonaws.com:6379/0"
    ),
    broker_use_ssl={"ssl_cert_reqs": ssl.CERT_NONE},
    redis_backend_use_ssl={"ssl_cert_reqs": ssl.CERT_NONE},
)

app.config_from_object(settings, namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
