from django.db import models


class GuerrillaDungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    start_time = models.CharField(default="", max_length=200)
    end_time = models.CharField(default=0, max_length=200)
    start_secs = models.FloatField(default=0)
    end_secs = models.FloatField(default=0)
    server = models.CharField(default="", max_length=10)
    group = models.CharField(default="", max_length=5)
    dungeon_id = models.IntegerField(default=-1)
    image_id = models.IntegerField(default=1)
    status = models.CharField(default="", max_length=15)
