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
        from blogs.models import Event
        
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

@shared_task(bind=True, max_retries=3)
def send_event_notifications(self):
    """Task to notify subscribers about upcoming events"""
    try:
        from blogs.models import Event, Subscriber
        
        server_now = localtime(timezone.now())
        three_days_later = server_now + timezone.timedelta(days=3)
        
        # Debug: Log time range
        logger.info(f"Checking events between {server_now} and {three_days_later}")
        
        upcoming_events = Event.objects.filter(
            startDate__gte=server_now,
            startDate__lte=three_days_later,
            ad=True
        )
        
        if not upcoming_events.exists():
            logger.info("No upcoming events found")
            return 0
            
        subscribers = Subscriber.objects.filter(notify=True)
        if not subscribers.exists():
            logger.info("No subscribers to notify")
            return 0
            
        success_count = 0
        for subscriber in subscribers:
            try:
                send_mail(
                    subject="Upcoming Events at Farmers Market",
                    message="",  # Text fallback
                    html_message=render_to_string(
                        'blogs/event_notification_email.html',
                        {'events': upcoming_events, 'subscriber': subscriber}
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {subscriber.email}: {str(e)}")
                
        logger.info(f"Sent {success_count}/{len(subscribers)} notifications")
        return success_count
        
    except Exception as e:
        logger.error(f"Notification task failed: {str(e)}")
        self.retry(exc=e, countdown=120)  # Longer retry for email tasks