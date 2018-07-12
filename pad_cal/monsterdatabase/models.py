from django.db import models


class ActiveSkill(models.Model):
    name = models.CharField(max_length=200,default="",blank=True)
    description = models.TextField(default="", blank=True,)
    levels = models.IntegerField(default=0)
    skillID = models.IntegerField()
    skillType = models.IntegerField()
    maxTurns = models.IntegerField()
    minTurns = models.IntegerField()



# Create your models here.
class Card(models.Model):
    activeSkill = models.OneToOneField(ActiveSkill)

