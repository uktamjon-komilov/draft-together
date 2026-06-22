from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import RegisterSerializer
from rooms.models import Room


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def rooms_page(request):
    return render(request, "rooms.html")


def room_page(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "room.html", {"room": room})


def accept_invite_page(request, token):
    return render(request, "accept_invite.html", {"token": token})
