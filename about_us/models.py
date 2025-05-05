from django.db import models

class OpsTeam(models.Model):
    member_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    image = models.ImageField()

class Hints(models.Model):
    member_name = models.ForeignKey(OpsTeam, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=50)

class Farmers(models.Model):
    farmer_name = models.CharField(max_length=50)
    farmer_job = models.CharField(max_length=50)
    success_story = models.TextField()
    
class Mission(models.Model):
    mission = models.CharField(max_length=50)

class Vission(models.Model):
    vission =  models.CharField(max_length=50)
