import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
    }


@pytest.fixture
def create_user(db):
    def _create_user(
        username="testuser", email="test@example.com", password="TestPass123!"
    ):
        return User.objects.create_user(
            username=username, email=email, password=password
        )

    return _create_user


@pytest.mark.django_db
class TestUserRegistration:
    """Tests for user registration endpoint."""

    def test_register_success(self, api_client, user_data):
        """Test successful user registration."""
        url = reverse("users:register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert response.data["user"]["username"] == user_data["username"]
        assert User.objects.filter(username=user_data["username"]).exists()

    def test_register_password_mismatch(self, api_client, user_data):
        """Test registration fails with password mismatch."""
        user_data["password_confirm"] = "DifferentPass123!"
        url = reverse("users:register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_email(self, api_client, user_data, create_user):
        """Test registration fails with duplicate email."""
        create_user()
        url = reverse("users:register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client, user_data):
        """Test registration fails with weak password."""
        user_data["password"] = "123"
        user_data["password_confirm"] = "123"
        url = reverse("users:register")
        response = api_client.post(url, user_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_success(self, api_client, create_user):
        """Test successful login returns JWT tokens."""
        user = create_user()
        url = reverse("users:login")
        response = api_client.post(
            url, {"username": user.username, "password": "TestPass123!"}, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, api_client, create_user):
        """Test login fails with invalid credentials."""
        create_user()
        url = reverse("users:login")
        response = api_client.post(
            url, {"username": "testuser", "password": "WrongPassword!"}, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCurrentUser:
    """Tests for current user endpoint."""

    def test_get_current_user_authenticated(self, api_client, create_user):
        """Test getting current user when authenticated."""
        user = create_user()
        api_client.force_authenticate(user=user)
        url = reverse("users:current_user")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user.username

    def test_get_current_user_unauthenticated(self, api_client):
        """Test getting current user fails when not authenticated."""
        url = reverse("users:current_user")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
