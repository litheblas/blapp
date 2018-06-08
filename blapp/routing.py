import django
from channels.routing import ProtocolTypeRouter

django.setup()

application = ProtocolTypeRouter({
    # http->django views is added by default
})
