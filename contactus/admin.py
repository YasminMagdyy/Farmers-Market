from django.contrib import admin
from .models import  Attendee, EventAttendee


admin.site.register(Attendee)
admin.site.register(EventAttendee)
