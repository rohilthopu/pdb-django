from django.db import models
from datetime import date


# class SkillEffect(models.Model):
#     effect = models.TextField(default="", max_length=200)


class Skill(models.Model):
    name = models.CharField(default="", max_length=50)
    altName = models.CharField(default="", max_length=50)
    effect = models.TextField(default="", max_length=200)


class Monster(models.Model):
    name = models.CharField(default="", max_length=50)
    hp = models.CharField(default="", max_length=20)
    defense = models.CharField(default="", max_length=20)
    atk = models.CharField(default="", max_length=20)
    jpnTitle = models.CharField(default="", max_length=50)
    altTitle = models.CharField(default="", max_length=50)
    altTitle2 = models.CharField(default="", max_length=50)
    dungeonID = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.name


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
    monsters = models.ManyToManyField(Monster)
    repeat = models.CharField(default="", max_length=10)

    def __str__(self):
        return self.altTitle


class DungeonToday(models.Model):
    dungeons = models.ManyToManyField(Dungeon)
    listingDate = models.DateField(default=date.today())
