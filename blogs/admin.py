from django.contrib import admin
from .models import Blog, Subscriber, Event

admin.site.register(Blog)

admin.site.register(Subscriber)
 
admin.site.register(Event)
