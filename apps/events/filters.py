import django_filters
from django.utils import timezone

from apps.events.models import Event


class EventFilter(django_filters.FilterSet):
    """
    Filter for events.

    Supports:
    - title: Search by title (case-insensitive contains)
    - location: Search by location (case-insensitive contains)
    - date_from: Events from this date
    - date_to: Events until this date
    - upcoming: Only future events (boolean)
    - organizer: Filter by organizer ID
    """

    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Title contains"
    )
    location = django_filters.CharFilter(
        field_name="location", lookup_expr="icontains", label="Location contains"
    )
    date_from = django_filters.DateTimeFilter(
        field_name="date", lookup_expr="gte", label="Date from"
    )
    date_to = django_filters.DateTimeFilter(
        field_name="date", lookup_expr="lte", label="Date to"
    )
    upcoming = django_filters.BooleanFilter(
        method="filter_upcoming", label="Only upcoming events"
    )
    organizer = django_filters.NumberFilter(
        field_name="organizer__id", label="Organizer ID"
    )

    class Meta:
        model = Event
        fields = ["title", "location", "date_from", "date_to", "upcoming"]

    def filter_upcoming(self, queryset, name, value):
        """Filter for upcoming events only."""
        if value:
            return queryset.filter(date__gt=timezone.now())
        return queryset
