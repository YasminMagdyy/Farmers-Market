from django.db import models

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

    def str(self):
        return self.email