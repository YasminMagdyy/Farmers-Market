# admin.py
from django.contrib import admin
from .models import Blog, Subscriber, BlogImage, Tag

class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    filter_horizontal = ['tags', 'saved_by']  # Makes managing tags and saved_by easier

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Subscriber)

