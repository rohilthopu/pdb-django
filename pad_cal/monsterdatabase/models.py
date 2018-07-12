from django.db import models


class LeaderSkill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True, )
    skillID = models.IntegerField(blank=True, default=0)
    skillType = models.IntegerField(blank=True, default=0)


# An active skill is just a specialized leader skill that can only be activated ever so often.
# As a result, inheritance is perfect here.
class ActiveSkill(LeaderSkill):
    levels = models.IntegerField(default=0)
    maxTurns = models.IntegerField(blank=True, default=0)
    minTurns = models.IntegerField(blank=True, default=0)


class MonsterData(models.Model):
    activeSkillID = models.IntegerField(blank=True)
    attributeID = models.IntegerField()
    baseID = models.IntegerField()
    cardID = models.IntegerField()
    cost = models.IntegerField()
    leaderSkillID = models.IntegerField(blank=True)
    maxATK = models.IntegerField()
    maxHP = models.IntegerField()
    maxLevel = models.IntegerField()
    maxRCV = models.IntegerField()
    minATK = models.IntegerField()
    minHP = models.IntegerField()
    minRCV = models.IntegerField()
    name = models.CharField(default="", max_length=200)
    rarity = models.IntegerField()


# Create your models here.
class CardNA(models.Model):
    activeSkill = models.OneToOneField(ActiveSkill, on_delete=models.CASCADE, related_name="active_skill", blank=True,
                                       null=True)
    leaderSkill = models.OneToOneField(LeaderSkill, on_delete=models.CASCADE, related_name="leader_skill", blank=True,
                                       null=True)
    monster = models.OneToOneField(MonsterData, on_delete=models.CASCADE, related_name="monster", blank=True,
                                   null=True)
