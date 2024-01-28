"""Use this for development"""

from .base import *

DEBUG = True
WSGI_APPLICATION = "core.wsgi.dev.application"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "support",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://*.localhost:3000",
    "http://*.localhost:3001",
    "http://localhost:3002",
]
CORS_ORIGIN_ALLOW_ALL = True
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
