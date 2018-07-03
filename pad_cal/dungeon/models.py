from django.db import models
from datetime import date

# Create your models here.
class Dungeon(models.Model):
    jpnTitle = models.CharField(default="", max_length=50)
    altTitle = models.CharField(default="", max_length=50)
    altTitle2 = models.CharField(default="", max_length=50)
    stamina = models.CharField(default="", max_length=10)
    battles = models.CharField(default="", max_length=10)
    dungeonType = models.CharField(default="", max_length=30)
    dungeonLink = models.TextField(default="")
    daily = models.BooleanField(default=False)

    def __str__(self):
        return self.jpnTitle

class DungeonToday(models.Model):
    dungeons = models.ManyToManyField(Dungeon)
    listingDate = models.DateField(default=date.today())