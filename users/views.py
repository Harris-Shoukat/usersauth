from rest_framework import generics
from django.contrib.auth import get_user_model
from .permissions import IsSuperAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserListSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    pass


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsSuperAdmin]