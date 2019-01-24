from django.db import models


# Create your models here.
class Version(models.Model):
    dungeon = models.IntegerField(default=-1)
    monster = models.IntegerField(default=-1)
    skill = models.IntegerField(default=-1)
