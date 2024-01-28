import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from decouple import config
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("ENVIRONMENT"))

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)
