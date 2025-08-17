# blogs/event_handlers.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from blogs.models import Event
from .tasks import update_event_statuses, send_event_notifications

@receiver(post_save, sender=Event)
def handle_event_save(sender, instance, created, **kwargs):
    if created:
        update_event_statuses.delay()
        if instance.ad:
            send_event_notifications.delay()