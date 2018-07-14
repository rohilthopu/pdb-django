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
    ancestorID = models.IntegerField(default=0)
    attributeID = models.IntegerField(default=0)
    baseID = models.IntegerField(default=0)
    cardID = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    inheritable = models.BooleanField(default=False)
    isCollab = models.BooleanField(default=False)
    isReleased = models.BooleanField(default=False)
    isUlt = models.BooleanField(default=False)
    leaderSkillID = models.IntegerField(blank=True)
    maxATK = models.IntegerField(default=0)
    maxHP = models.IntegerField(default=0)
    maxLevel = models.IntegerField(default=0)
    maxRCV = models.IntegerField(default=0)
    minATK = models.IntegerField(default=0)
    minHP = models.IntegerField(default=0)
    minRCV = models.IntegerField(default=0)
    maxXP = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=200)
    rarity = models.IntegerField(default=0)
    subAttributeID = models.IntegerField(default=0)
    hp99 = models.IntegerField(default=0)
    atk99 = models.IntegerField(default=0)
    rcv99 = models.IntegerField(default=0)
    nextEvo = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Create your models here.
class CardNA(models.Model):
    activeSkill = models.ManyToManyField(ActiveSkill)
    leaderSkill = models.ManyToManyField(LeaderSkill)
    monster = models.OneToOneField(MonsterData, on_delete=models.CASCADE, related_name="monster", blank=True,
                                   null=True)

    def __str__(self):
        return self.monster.name
