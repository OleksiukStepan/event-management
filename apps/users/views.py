import logging

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.schemas import AUTH_SCHEMAS, USER_SCHEMAS
from apps.users.serializers import UserRegistrationSerializer, UserSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(post=AUTH_SCHEMAS["register"])
class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user.

    Creates a new user account. No authentication required.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"User registered successfully: {user.username}")
        return Response(
            {
                "message": "User registered successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(get=USER_SCHEMAS["current_user"])
class CurrentUserView(APIView):
    """Get current authenticated user's profile."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
