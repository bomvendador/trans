from channels import route
from trans.consumers import ws_connect, ws_disconnect
from django.contrib.auth.models import User

channel_routing = [
   # Wire up websocket channels to our consumers:
   route("websocket.connect", User.ws_connect),
   route("websocket.receive", User.ws_receive),
]