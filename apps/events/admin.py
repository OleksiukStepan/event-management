from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.events.models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = [
        "id",
        "title",
        "date",
        "location",
        "organizer",
        "participants_count",
    ]
    list_display_links = ["id", "title"]
    list_filter = ["date", "location"]
    search_fields = ["title", "description", "location"]
    search_help_text = "Search by title, description, or location"
    date_hierarchy = "date"
    readonly_fields = ["created_at", "updated_at"]

    def participants_count(self, obj):
        return obj.registrations.count()

    participants_count.short_description = "Participants"


@admin.register(EventRegistration)
class EventRegistrationAdmin(ModelAdmin):
    list_display = ["id", "user", "event", "registered_at"]
    list_display_links = ["id", "user"]
    list_filter = ["registered_at", "event"]
    search_fields = ["user__username", "user__email", "event__title"]
    search_help_text = "Search by username, email, or event title"
    date_hierarchy = "registered_at"
