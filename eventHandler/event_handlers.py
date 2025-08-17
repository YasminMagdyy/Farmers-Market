# blogs/event_handlers.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from contactus.models import Event
from .tasks import update_event_statuses

@receiver(post_save, sender=Event)
def handle_event_save(sender, instance, created, **kwargs):
    if created:
        update_event_statuses.delay()
