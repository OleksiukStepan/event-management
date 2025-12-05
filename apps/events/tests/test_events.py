from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.events.models import Event, EventRegistration


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def _create_user(
        username="testuser", email="test@example.com", password="TestPass123!"
    ):
        return User.objects.create_user(
            username=username, email=email, password=password
        )

    return _create_user


@pytest.fixture
def create_event(db, create_user):
    def _create_event(
        title="Test Event",
        description="Test Description",
        date=None,
        location="Test Location",
        organizer=None,
    ):
        if date is None:
            date = timezone.now() + timedelta(days=7)
        if organizer is None:
            organizer = create_user()
        return Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            organizer=organizer,
        )

    return _create_event


@pytest.mark.django_db
class TestEventList:
    """Tests for event list endpoint."""

    def test_list_events_unauthenticated(self, api_client, create_event):
        """Test listing events without authentication."""
        create_event()
        url = reverse("events:event-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_list_events_with_filter(self, api_client, create_event):
        """Test filtering events by title."""
        create_event(title="Python Conference")
        create_event(
            title="JavaScript Meetup",
            organizer=User.objects.create_user(
                username="user2", email="u2@test.com", password="pass123!"
            ),
        )
        url = reverse("events:event-list")
        response = api_client.get(url, {"title": "Python"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert "Python" in response.data["results"][0]["title"]


@pytest.mark.django_db
class TestEventCreate:
    """Tests for event creation endpoint."""

    def test_create_event_authenticated(self, api_client, create_user):
        """Test creating event when authenticated."""
        user = create_user()
        api_client.force_authenticate(user=user)
        url = reverse("events:event-list")
        data = {
            "title": "New Event",
            "description": "Event description",
            "date": (timezone.now() + timedelta(days=7)).isoformat(),
            "location": "Test Location",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.filter(title="New Event").exists()

    def test_create_event_unauthenticated(self, api_client):
        """Test creating event fails without authentication."""
        url = reverse("events:event-list")
        data = {
            "title": "New Event",
            "description": "Event description",
            "date": (timezone.now() + timedelta(days=7)).isoformat(),
            "location": "Test Location",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestEventUpdate:
    """Tests for event update endpoint."""

    def test_update_event_by_organizer(self, api_client, create_user):
        """Test organizer can update their event."""
        user = create_user()
        event = Event.objects.create(
            title="Original Title",
            description="Description",
            date=timezone.now() + timedelta(days=7),
            location="Location",
            organizer=user,
        )
        api_client.force_authenticate(user=user)
        url = reverse("events:event-detail", kwargs={"pk": event.pk})
        response = api_client.patch(url, {"title": "Updated Title"}, format="json")

        assert response.status_code == status.HTTP_200_OK
        event.refresh_from_db()
        assert event.title == "Updated Title"

    def test_update_event_by_non_organizer(self, api_client, create_user):
        """Test non-organizer cannot update event."""
        organizer = create_user()
        other_user = User.objects.create_user(
            username="other", email="other@test.com", password="pass123!"
        )
        event = Event.objects.create(
            title="Original Title",
            description="Description",
            date=timezone.now() + timedelta(days=7),
            location="Location",
            organizer=organizer,
        )
        api_client.force_authenticate(user=other_user)
        url = reverse("events:event-detail", kwargs={"pk": event.pk})
        response = api_client.patch(url, {"title": "Updated Title"}, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestEventRegistration:
    """Tests for event registration endpoints."""

    def test_register_for_event(self, api_client, create_user, create_event):
        """Test user can register for an event."""
        user = create_user()
        event = create_event(
            organizer=User.objects.create_user(
                username="org", email="org@test.com", password="pass123!"
            )
        )
        api_client.force_authenticate(user=user)
        url = reverse("events:event-register", kwargs={"pk": event.pk})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert EventRegistration.objects.filter(user=user, event=event).exists()

    def test_register_twice_fails(self, api_client, create_user, create_event):
        """Test user cannot register twice for same event."""
        user = create_user()
        event = create_event(
            organizer=User.objects.create_user(
                username="org", email="org@test.com", password="pass123!"
            )
        )
        EventRegistration.objects.create(user=user, event=event)
        api_client.force_authenticate(user=user)
        url = reverse("events:event-register", kwargs={"pk": event.pk})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unregister_from_event(self, api_client, create_user, create_event):
        """Test user can unregister from an event."""
        user = create_user()
        event = create_event(
            organizer=User.objects.create_user(
                username="org", email="org@test.com", password="pass123!"
            )
        )
        EventRegistration.objects.create(user=user, event=event)
        api_client.force_authenticate(user=user)
        url = reverse("events:event-register", kwargs={"pk": event.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not EventRegistration.objects.filter(user=user, event=event).exists()

    def test_unregister_when_not_registered(
        self, api_client, create_user, create_event
    ):
        """Test unregister fails when user is not registered."""
        user = create_user()
        event = create_event(
            organizer=User.objects.create_user(
                username="org", email="org@test.com", password="pass123!"
            )
        )
        api_client.force_authenticate(user=user)
        url = reverse("events:event-register", kwargs={"pk": event.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_participants(self, api_client, create_event, create_user):
        """Test listing event participants."""
        event = create_event()
        user1 = create_user(username="user1", email="u1@test.com", password="pass123!")
        user2 = User.objects.create_user(
            username="user2", email="u2@test.com", password="pass123!"
        )
        EventRegistration.objects.create(user=user1, event=event)
        EventRegistration.objects.create(user=user2, event=event)

        url = reverse("events:event-participants", kwargs={"pk": event.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
