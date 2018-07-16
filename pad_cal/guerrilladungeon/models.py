from django.db import models

# Create your models here.

class GuerrillaDungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    startTime = models.IntegerField(default=0)
    endTime = models.IntegerField(default=0)
    server = models.CharField(default="", max_length=10)
    group = models.CharField(default="", max_length=5)