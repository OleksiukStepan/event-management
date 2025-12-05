import logging

from django.conf import settings
from django.core.mail import send_mail

from apps.events.models import EventRegistration

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for sending email notifications."""

    @staticmethod
    def send_registration_confirmation(registration: EventRegistration):
        """
        Send email confirmation when user registers for an event.
        """
        user = registration.user
        event = registration.event

        subject = f"Registration Confirmed: {event.title}"
        message = (
            f"Hello {user.username},\n\n"
            f"You have successfully registered for the event:\n\n"
            f"Title: {event.title}\n"
            f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Location: {event.location}\n\n"
            f"See you there!\n"
            f"Event Management Team"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(
                f"Registration email sent to {user.email} " f"for event {event.title}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send registration email to {user.email}: {e}")
            return False

    @staticmethod
    def send_unregistration_notification(user, event):
        """
        Send email when user unregisters from an event.
        """
        subject = f"Unregistered from: {event.title}"
        message = (
            f"Hello {user.username},\n\n"
            f"You have been unregistered from the event:\n\n"
            f"Title: {event.title}\n"
            f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n\n"
            f"We hope to see you at other events!\n"
            f"Event Management Team"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(
                f"Unregistration email sent to {user.email} " f"for event {event.title}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send unregistration email to {user.email}: {e}")
            return False
