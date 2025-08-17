from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

# Functions

def get_next_thursday_time(hour, minute=0):
    today = datetime.date.today()
    weekday = today.weekday()  # Monday=0, Thursday=3
    days_until_thursday = (3 - weekday + 7) % 7
    if days_until_thursday == 0:  # If today is Thursday, go to next week
        days_until_thursday = 7
    next_thursday = today + datetime.timedelta(days=days_until_thursday)
    return datetime.datetime.combine(next_thursday, datetime.time(hour, minute))

def get_next_thursday_8am():
    return get_next_thursday_time(8, 0) 

def get_next_thursday_3pm():
    return get_next_thursday_time(15, 0)

#  Models

class Specializations(models.Model):
    specialization = models.CharField(max_length=50)

class Booths(models.Model):
    boothNumber = models.IntegerField()
    boothName = models.CharField(max_length=50)

class Farmer(models.Model):
    farmerName = models.CharField(max_length=50)
    farmerSpecialization = models.ForeignKey(Specializations, on_delete=models.CASCADE)
    farmerBreif = models.TextField(max_length=200)
    farmerImage = models.ImageField()

class FarmersInBooths(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booths, on_delete=models.CASCADE)
    
class Products(models.Model):
    productName = models.CharField(max_length=50)
    
class ProductPrices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    productPrice = models.FloatField()
    editDeadlineDateTime = models.DateTimeField(default=get_next_thursday_8am)

    def clean(self):
        # Only check on update
        if self.pk and timezone.now() > self.editDeadlineDateTime:
            raise ValidationError('Cannot edit this old entry')

    class Meta:
        unique_together = ('product', 'productPrice')


class FarmerProducts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    
class Mission(models.Model):
    mission = models.TextField(max_length=50)

class Vission(models.Model):
    vission =  models.TextField(max_length=50)

class TeamMemebers(models.Model):
    memberName = models.CharField(max_length=50)
    memberPosition = models.CharField(max_length=50)
    memberBreif = models.CharField(max_length=50)
    memberPhoto = models.ImageField()

class ThursdayMarket(models.Model):
    startDateTime = models.DateTimeField(default=get_next_thursday_8am())
    endDateTime = models.DateTimeField(default=get_next_thursday_3pm())