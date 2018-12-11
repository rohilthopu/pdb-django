from django.db import models


class Floor(models.Model):
    floorNumber = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=100)
    stamina = models.IntegerField(default=0)
    battles = models.IntegerField(default=0)


class Dungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    dungeonID = models.IntegerField(default=0)
    dungeonType = models.CharField(default="", max_length=50)
    floorName = models.CharField(default="", max_length=50)
    floorCount = models.IntegerField(default=0)
    possibleDrops = models.TextField(default="")