from django.db import models


# Create your models here.

class GuerrillaDungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    startTime = models.CharField(default="", max_length=200)
    endTime = models.CharField(default=0, max_length=200)
    startSecs = models.FloatField(default=0)
    endSecs = models.FloatField(default=0)
    server = models.CharField(default="", max_length=10)
    group = models.CharField(default="", max_length=5)
    dungeon_id = models.IntegerField(default=-1)
    image_id = models.IntegerField(default=1)
