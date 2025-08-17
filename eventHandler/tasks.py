from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import localtime
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)  # Added retry capability
def update_event_statuses(self):
    """Task to automatically close event registrations when deadline passes"""
    try:
        from contactus.models import Event
        
        # Debug: Log current time comparison
        server_now = localtime(timezone.now())
        logger.info(f"Running status update at server time: {server_now}")
        
        # Get events that should be closed
        expired_events = Event.objects.filter(
            eventClosedRegistration__lte=server_now,
            eventRegistrationStatus="OPEN_FOR_REGISTRATION"
        )
        
        # Debug: Log affected events
        logger.info(f"Found {expired_events.count()} events to close")
        
        # Perform update and log results
        updated = expired_events.update(
            eventRegistrationStatus="CLOSED_REGISTRATION"
        )
        logger.info(f"Successfully closed {updated} events")
        
        return updated
        
    except Exception as e:
        logger.error(f"Failed to update event statuses: {str(e)}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds

