import requests
from rest_framework import generics
from django.contrib.auth import get_user_model
from .permissions import IsSuperAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserListSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.external_api import get_google_suggestions

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsSuperAdmin]


class ProfileUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class GoogleSuggestionsView(APIView):

    def get(self, request):
        requested_query = request.query_params.get("q", "")
        
        if not requested_query:
            return Response(
                {"error": "Query is required."},
                status = status.HTTP_400_BAD_REQUEST,
            )

        try:
            suggestions = get_google_suggestions(requested_query)

            return Response({
                "query": requested_query,
                "suggestions": suggestions,
            })

        except requests.Timeout:
            return Response(
                {"detail": "suggestions request timed out."},
                status = status.HTTP_504_GATEWAY_TIMEOUT,
            )

        except requests.RequestException:
            return Response(
                {"detail": "Unable to fetch search suggestions."},
                status = status.HTTP_502_BAD_GATEWAY,
            )
