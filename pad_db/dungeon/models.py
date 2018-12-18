from django.db import models


class Floor(models.Model):
    floorNumber = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=100)
    stamina = models.IntegerField(default=0)
    battles = models.IntegerField(default=0)
    possibleDrops = models.TextField(default="")
    dungeonID = models.IntegerField(default=0)
    requiredDungeon = models.IntegerField(default=0)
    modifiers = models.TextField(default="")
    entryRequirement = models.TextField(default="")


class Dungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    dungeonID = models.IntegerField(default=0)
    dungeonType = models.CharField(default="", max_length=50)
    floorCount = models.IntegerField(default=0)
