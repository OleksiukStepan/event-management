from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import CurrentUserView, UserRegistrationView

app_name = "users"

urlpatterns = [
    # Registration
    path("register/", UserRegistrationView.as_view(), name="register"),
    # JWT Authentication
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User profile
    path("me/", CurrentUserView.as_view(), name="current_user"),
]
