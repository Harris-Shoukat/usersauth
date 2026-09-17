from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, UserListView, ProfileUpdateView


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "users/",
        UserListView.as_view(),
        name="users-list",
    ),

    path(
        "profile/",
        ProfileUpdateView.as_view(),
        name="profile",
    ),
]