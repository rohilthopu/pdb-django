from django.db import models

# Create your models here.

class Dungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    dungeonID = models.IntegerField(default=0)
    startTime = models.FloatField(default=0)
    endTime = models.FloatField(default=0)

    # bonus info
    bonusName = models.CharField(default="", max_length=100)
    bonusStart = models.FloatField(default=0)
    bonusEnd = models.FloatField(default=0)