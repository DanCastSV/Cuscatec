import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cuscatec.settings')

# Inicializar Django PRIMERO
django_asgi_app = get_asgi_application()

# DESPUÉS importar Channels y routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cusca.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cusca.routing.websocket_urlpatterns
        )
    ),
})
