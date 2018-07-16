from django.db import models

# Create your models here.

class GuerrillaDungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    startTime = models.CharField(default="", max_length=200)
    endTime = models.CharField(default=0, max_length=200)
    server = models.CharField(default="", max_length=10)
    group = models.CharField(default="", max_length=5)