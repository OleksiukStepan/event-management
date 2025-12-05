import logging

from drf_spectacular.utils import extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.exceptions import AlreadyRegisteredError, NotRegisteredError
from apps.events.filters import EventFilter
from apps.events.models import Event, EventRegistration
from apps.events.permissions import IsOrganizerOrReadOnly
from apps.events.schemas import EVENT_SCHEMAS, REGISTRATION_SCHEMAS
from apps.events.serializers import (
    EventCreateUpdateSerializer,
    EventDetailSerializer,
    EventListSerializer,
    ParticipantSerializer,
)
from apps.events.services import EmailNotificationService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=EVENT_SCHEMAS["list"],
    retrieve=EVENT_SCHEMAS["retrieve"],
    create=EVENT_SCHEMAS["create"],
    update=EVENT_SCHEMAS["update"],
    partial_update=EVENT_SCHEMAS["partial_update"],
    destroy=EVENT_SCHEMAS["destroy"],
)
class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event CRUD operations.

    Provides list, create, retrieve, update, and delete actions.
    Includes filtering by title, location, date, and upcoming status.
    """

    queryset = Event.objects.select_related("organizer").all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOrganizerOrReadOnly,
    ]
    filterset_class = EventFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["date", "created_at", "title"]
    ordering = ["-date"]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return EventListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return EventCreateUpdateSerializer
        return EventDetailSerializer

    def perform_create(self, serializer):
        """Log event creation."""
        event = serializer.save()
        logger.info(f"Event created: {event.title} by {self.request.user.username}")

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def register(self, request, pk=None):
        """Register or unregister current user for the event."""
        event = self.get_object()
        user = request.user

        if request.method == "POST":
            if EventRegistration.objects.filter(user=user, event=event).exists():
                raise AlreadyRegisteredError()

            registration = EventRegistration.objects.create(user=user, event=event)
            EmailNotificationService.send_registration_confirmation(registration)

            logger.info(f"User {user.username} registered for: {event.title}")
            return Response(
                {"detail": "Successfully registered for the event."},
                status=status.HTTP_201_CREATED,
            )

        # DELETE
        try:
            registration = EventRegistration.objects.get(user=user, event=event)
            registration.delete()
            EmailNotificationService.send_unregistration_notification(user, event)
            logger.info(f"User {user.username} unregistered from: {event.title}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventRegistration.DoesNotExist:
            raise NotRegisteredError()

    @REGISTRATION_SCHEMAS["participants"]
    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        """List all participants registered for the event."""
        event = self.get_object()
        registrations = event.registrations.select_related("user").all()
        serializer = ParticipantSerializer(registrations, many=True)
        return Response(serializer.data)
