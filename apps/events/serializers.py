from django.contrib.auth.models import User
from rest_framework import serializers

from apps.events.models import Event, EventRegistration


class OrganizerSerializer(serializers.ModelSerializer):
    """Minimal user serializer for organizer info."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = fields


class EventListSerializer(serializers.ModelSerializer):
    """Serializer for event list view."""

    organizer = OrganizerSerializer(read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "date",
            "location",
            "organizer",
            "participants_count",
            "is_upcoming",
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    """Serializer for event detail view."""

    organizer = OrganizerSerializer(read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "participants_count",
            "is_upcoming",
            "is_registered",
            "created_at",
            "updated_at",
        ]

    def get_is_registered(self, obj):
        """Check if current user is registered for this event."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.registrations.filter(user=request.user).exists()
        return False


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating events."""

    class Meta:
        model = Event
        fields = ["id", "title", "description", "date", "location"]

    def create(self, validated_data):
        """Set organizer to current user."""
        validated_data["organizer"] = self.context["request"].user
        return super().create(validated_data)


class EventRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for event registration."""

    user = OrganizerSerializer(read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)

    class Meta:
        model = EventRegistration
        fields = ["id", "user", "event", "event_title", "registered_at"]
        read_only_fields = ["id", "user", "registered_at"]


class ParticipantSerializer(serializers.ModelSerializer):
    """Serializer for listing event participants."""

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = EventRegistration
        fields = ["id", "username", "email", "registered_at"]
