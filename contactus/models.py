from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
from django.db import models


class Event(models.Model):
    EVENT_REGISTRATION_STATUS_CHOICES = [
        ("OPEN_FOR_REGISTRATION", "OPEN_FOR_REGISTRATION"),
        ("CLOSED_REGISTRATION", "CLOSED_REGISTRATION"),
    ] 
    
    # Event Description and name
    eventName = models.CharField(max_length=50)
    eventDescription = models.TextField(max_length=200)

    startDate = models.DateTimeField(null=False, blank=False)
    endDate = models.DateTimeField(null=False, blank=False)
    
    # Date where the registration date is closed
    eventClosedRegistartion = models.DateTimeField(null=False, blank=False)

    eventRegistrationStatus = models.CharField(max_length=50 ,choices=EVENT_REGISTRATION_STATUS_CHOICES, default="OPEN_FOR_REGISTRATION")

    ad = models.BooleanField(null=False, blank=False)

    class Meta:
        unique_together = ("eventName", "startDate", "endDate")
    

class Attendee(models.Model):
    attendeeName = models.CharField(max_length=50)
    phoneNumber = models.CharField()

    
    class Meta:
        unique_together = ("attendeeName", "phoneNumber")


class EventAttendee(models.Model):
    eventName = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendeeName = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("attendeeName", "eventName")