from django.urls import path

from .views import RoomsAPIView, RoomInviteAPIView, AcceptInviteAPIView


urlpatterns = [
    path("rooms/", RoomsAPIView.as_view()),
    path("rooms/<str:room_id>/invites/", RoomInviteAPIView.as_view()),
    path("invites/<str:token>/accept/", AcceptInviteAPIView.as_view()),
]
