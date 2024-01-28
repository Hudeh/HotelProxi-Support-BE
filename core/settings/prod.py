"""Use this for production"""
from .base import *
import dj_database_url
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk

DEBUG = config("DEBUG", default=False, cast=bool)
# database
DATABASES = {
    "default": dj_database_url.config(
        "DATABASE_URL", conn_max_age=600, ssl_require=True
    )
}
ALLOWED_HOSTS += ["nsc-test-api-6c116123a4d7.herokuapp.com"]
WSGI_APPLICATION = "core.wsgi.prod.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "https://support.hotelproxi.com",
)
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.hotelproxi.com$",
    r"^https://\w+\.herokuapp.com$",
    r"^http://\w+\:3000$",
    r"^http://\w+\:3001$",
    r"^http://\w+\:3002$",
]
CORS_ORIGIN_ALLOW_ALL = False
# enforce https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_URL")],
        },
    },
}

sentry_sdk.init(
    dsn=config("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
# s3 static settings
STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "core.settings.storage_backends.StaticStorage"
# s3 public media settings
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "core.settings.storage_backends.PublicMediaStorage"
# s3 private media settings
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "core.settings.storage_backends.PrivateMediaStorage"
