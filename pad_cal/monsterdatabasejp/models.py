from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True, )
    skillID = models.IntegerField(blank=True, default=0)
    skillType = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True


class LeaderSkill(Skill):
    # literally just a placeholder to get the model to work using inheritance
    doesNothing = models.BooleanField(default=False)


# An active skill is just a specialized leader skill that can only be activated ever so often.
# As a result, inheritance is perfect here.
class ActiveSkill(Skill):
    levels = models.IntegerField(default=0)
    maxTurns = models.IntegerField(blank=True, default=0)
    minTurns = models.IntegerField(blank=True, default=0)


class Evolution(models.Model):
    evo = models.IntegerField(default=0)

    def __str__(self):
        return str(self.evo)


class MonsterData(models.Model):
    activeSkillID = models.IntegerField(blank=True, default=0)
    ancestorID = models.IntegerField(default=0)
    attributeID = models.IntegerField(default=0)
    attribute = models.CharField(default="", max_length=100)

    awakenings = models.TextField(default="")

    baseID = models.IntegerField(default=0)
    cardID = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    # JP only applicable
    furigana = models.CharField(default="", max_length=100)

    inheritable = models.BooleanField(default=False)
    isCollab = models.BooleanField(default=False)
    isReleased = models.BooleanField(default=False)
    isUlt = models.BooleanField(default=False)
    leaderSkillID = models.IntegerField(blank=True, default=0)
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
    subattribute = models.CharField(default="", max_length=100)
    hp99 = models.IntegerField(default=0)
    atk99 = models.IntegerField(default=0)
    rcv99 = models.IntegerField(default=0)

    superAwakenings = models.TextField(default="")

    evolutions = models.ManyToManyField(Evolution)

    evomat1 = models.IntegerField(default=0)
    evomat2 = models.IntegerField(default=0)
    evomat3 = models.IntegerField(default=0)
    evomat4 = models.IntegerField(default=0)
    evomat5 = models.IntegerField(default=0)

    unevomat1 = models.IntegerField(default=0)
    unevomat2 = models.IntegerField(default=0)
    unevomat3 = models.IntegerField(default=0)
    unevomat4 = models.IntegerField(default=0)
    unevomat5 = models.IntegerField(default=0)

    type1 = models.CharField(default="", max_length=100)
    type2 = models.CharField(default="", max_length=100)
    type3 = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.name


class CardJP(models.Model):
    activeSkill = models.ManyToManyField(ActiveSkill)
    leaderSkill = models.ManyToManyField(LeaderSkill)
    monster = models.OneToOneField(MonsterData, on_delete=models.CASCADE, related_name="monster", blank=True,
                                   null=True)

    def __str__(self):
        return self.monster.name
