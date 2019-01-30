from django.db import models


class Floor(models.Model):
    floorNumber = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=100)
    stamina = models.IntegerField(default=0)
    waves = models.IntegerField(default=0)
    possibleDrops = models.TextField(default="")
    dungeonID = models.IntegerField(default=0)
    requiredDungeon = models.IntegerField(default=0)
    requiredFloor = models.IntegerField(default=0)
    encounterModifiers = models.TextField(default="")
    teamModifiers = models.TextField(default="")
    entryRequirement = models.TextField(default="")
    otherModifier = models.TextField(default="")
    messages = models.TextField(default="")
    score = models.IntegerField(default=0)
    fixedTeam = models.TextField(default="")
    remainingModifiers = models.TextField(default="")
    enhancedType = models.CharField(default=0, max_length=100)
    enhancedAttribute = models.CharField(default=0, max_length=100)
    imageID = models.IntegerField(default=0)


class Dungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    dungeonID = models.IntegerField(default=0)
    dungeonType = models.CharField(default="", max_length=50)
    floorCount = models.IntegerField(default=0)
    imageID = models.IntegerField(default=0)
