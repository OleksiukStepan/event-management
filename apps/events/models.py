import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Event(models.Model):
    """
    Event model representing conferences, meetups, etc.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300, blank=True, null=True)
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        """Check if event is in the future."""
        return self.date > timezone.now()

    @property
    def participants_count(self):
        """Get number of registered participants."""
        return self.registrations.count()


class EventRegistration(models.Model):
    """
    Model for user registration to events.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_registrations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "event"]
        ordering = ["-registered_at"]
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(
                f"User {self.user.username} registered for event: "
                f"{self.event.title}"
            )
