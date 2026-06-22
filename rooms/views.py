from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nanoid import generate

from .models import Room, RoomInvite, RoomMember
from .serializers import RoomCreateSerializer, RoomSerializer


class RoomsAPIView(APIView):
    def get(self, request):
        rooms = Room.objects.filter(owner=request.user)
        return Response(RoomSerializer(rooms, many=True).data)

    def post(self, request):
        serializer = RoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save(owner=request.user)
        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


class RoomInviteAPIView(APIView):
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id, owner=request.user)
        invite = RoomInvite.objects.create(
            room=room,
            created_by=request.user,
            token=generate(size=24),
        )
        return Response({"token": invite.token}, status=status.HTTP_201_CREATED)


class AcceptInviteAPIView(APIView):
    def post(self, request, token):
        invite = get_object_or_404(RoomInvite, token=token)

        if not invite.is_valid():
            return Response({"detail": "This invite is no longer valid."}, status=status.HTTP_410_GONE)

        if invite.room.owner == request.user:
            return Response({"room_id": invite.room.id})

        _, created = RoomMember.objects.get_or_create(
            room=invite.room,
            user=request.user,
            defaults={"invite": invite},
        )

        return Response({"room_id": invite.room.id}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
