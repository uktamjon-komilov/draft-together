from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

from channels.db import database_sync_to_async



@database_sync_to_async
def get_user(token_key: str):
    try:
        return Token.objects.select_related("user").get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        qs = parse_qs(scope["query_string"].decode())
        token_key = qs.get("token", [None])[0]
        scope["user"] = await get_user(token_key)
        return await self.app(scope, receive, send)
