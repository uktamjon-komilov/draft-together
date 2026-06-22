from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from config.models import TimestampModel


UserModel = get_user_model()


class Room(TimestampModel):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="rooms")


class RoomMember(TimestampModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="room_memberships")
    invite = models.ForeignKey("RoomInvite", null=True, on_delete=models.SET_NULL, related_name="members")

    class Meta:
        unique_together = ["room", "user"]


class RoomInvite(TimestampModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="invites")
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="created_invites")
    token = models.CharField(max_length=32, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
