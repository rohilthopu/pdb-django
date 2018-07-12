from django.db import models


class LeaderSkill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True, )
    skillID = models.IntegerField(blank=True,)
    skillType = models.IntegerField(blank=True,)

# An active skill is just a specialized leader skill that can only be activated ever so often.
# As a result, inheritance is perfect here.
class ActiveSkill(LeaderSkill):
    levels = models.IntegerField(default=0)
    maxTurns = models.IntegerField(blank=True)
    minTurns = models.IntegerField(blank=True)





# Create your models here.
class CardNA(models.Model):
    activeSkill = models.OneToOneField(ActiveSkill, on_delete=models.CASCADE, related_name="active_skill", blank=True)


