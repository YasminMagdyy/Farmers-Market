
from django.db import models
from eventHandler.tasks import update_event_statuses
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogImage(models.Model):
    blog = models.ForeignKey('Blog', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('ceremony', 'Ceremonies'),
        ('visit', 'Visits'),
    ]

    name = models.CharField(max_length=200)
    created_date = models.DateField()
    description = models.TextField()
    main_image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )
    saved_by = models.ManyToManyField(User, related_name='saved_blogs', blank=True)

    def str(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    notify = models.BooleanField(default=False)

    def str(self):
        return self.email

