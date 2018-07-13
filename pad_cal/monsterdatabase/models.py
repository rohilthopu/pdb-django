from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True,)
    skillID = models.IntegerField(blank=True, default=0)
    skillType = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True

class LeaderSkill(Skill):
    # literally just a placeholder to get the model to work
    doesNothing = models.BooleanField(default=False)

# An active skill is just a specialized leader skill that can only be activated ever so often.
# As a result, inheritance is perfect here.
class ActiveSkill(Skill):
    levels = models.IntegerField(default=0)
    maxTurns = models.IntegerField(blank=True, default=0)
    minTurns = models.IntegerField(blank=True, default=0)


class MonsterData(models.Model):
    activeSkillID = models.IntegerField(blank=True)
    ancestorID = models.IntegerField()
    attributeID = models.IntegerField()
    baseID = models.IntegerField()
    cardID = models.IntegerField()
    cost = models.IntegerField()
    inheritable = models.BooleanField()
    isCollab = models.BooleanField()
    isReleased = models.BooleanField()
    isUlt = models.BooleanField()
    leaderSkillID = models.IntegerField(blank=True)
    maxATK = models.IntegerField()
    maxHP = models.IntegerField()
    maxLevel = models.IntegerField()
    maxRCV = models.IntegerField()
    minATK = models.IntegerField()
    minHP = models.IntegerField()
    minRCV = models.IntegerField()
    maxXP = models.IntegerField()
    name = models.CharField(default="", max_length=200)
    rarity = models.IntegerField()
    subAttributeID = models.IntegerField()


# Create your models here.
class CardNA(models.Model):
    activeSkill = models.ManyToManyField(ActiveSkill)
    leaderSkill = models.ManyToManyField(LeaderSkill)
    monster = models.OneToOneField(MonsterData, on_delete=models.CASCADE, related_name="monster", blank=True,
                                   null=True)
