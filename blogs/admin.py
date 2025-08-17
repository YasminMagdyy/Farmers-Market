from django.contrib import admin
from .models import Blog, Subscriber, Event,BlogImage
 
admin.site.register(Event)
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    filter_horizontal = ['saved_by']

admin.site.register(Subscriber)
