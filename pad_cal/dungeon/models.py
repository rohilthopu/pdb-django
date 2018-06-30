from django.db import models

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
