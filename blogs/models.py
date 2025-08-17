# blogs/models.py
from django.db import models
from eventHandler.tasks import update_event_statuses, send_event_notifications

class Blog(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    
    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    notify = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Event(models.Model):
    EVENT_REGISTRATION_STATUS_CHOICES = [
        ("OPEN_FOR_REGISTRATION", "Open for registration"),
        ("CLOSED_REGISTRATION", "Closed registration"),
    ]
    
    eventName = models.CharField(max_length=50)
    eventDescription = models.TextField(max_length=200)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    eventClosedRegistration = models.DateTimeField()
    eventRegistrationStatus = models.CharField(
        max_length=50, 
        choices=EVENT_REGISTRATION_STATUS_CHOICES
    )
    ad = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # True if creating, False if updating
        super().save(*args, **kwargs)  # Save first
        
        if is_new or self.ad:  # ← Runs for new OR when `ad` is True
            update_event_statuses.delay()
            if self.ad:
                send_event_notifications.delay()

    class Meta:
        unique_together = ("eventName", "startDate", "endDate")

    def __str__(self):
        return self.eventName 