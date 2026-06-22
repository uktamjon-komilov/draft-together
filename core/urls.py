from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("rooms/", views.rooms_page, name="rooms"),
    path("rooms/<str:room_id>/", views.room_page, name="room"),
    path("invite/<str:token>/", views.accept_invite_page, name="accept-invite"),
    path("api/auth/register/", views.RegisterAPIView.as_view(), name="api-register"),
]
