# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

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
    tags = models.ManyToManyField(Tag, blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_blogs', blank=True)
    
    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    notify = models.BooleanField(default=False)

    def __str__(self):
        return self.email