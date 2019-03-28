from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True, )
    skillID = models.IntegerField(default=-1)
    skill_type = models.CharField(max_length=50, default="")
    hp_mult = models.FloatField(default=1)
    atk_mult = models.FloatField(default=1)
    rcv_mult = models.FloatField(default=1)
    dmg_reduction = models.FloatField(default=0)

    # connected skills
    c_skill_1 = models.IntegerField(default=-1)
    c_skill_2 = models.IntegerField(default=-1)
    c_skill_3 = models.IntegerField(default=-1)

    # skill type
    skill_class = models.CharField(max_length=100, default="")

    levels = models.IntegerField(default=0)
    maxTurns = models.IntegerField(blank=True, default=0)
    minTurns = models.IntegerField(blank=True, default=0)


class Evolution(models.Model):
    evo = models.IntegerField(default=0)

    def __str__(self):
        return str(self.evo)


class Monster(models.Model):
    activeSkillID = models.IntegerField(blank=True, default=0)
    ancestorID = models.IntegerField(default=0)
    attributeID = models.IntegerField(default=0)
    attribute = models.CharField(default="", max_length=100)

    awakenings = models.TextField(default="")
    awakenings_raw = models.TextField(default="")

    baseID = models.IntegerField(default=0)
    cardID = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    inheritable = models.CharField(default="", max_length=5)
    isCollab = models.CharField(default="", max_length=5)
    isReleased = models.CharField(default="", max_length=5)
    isUlt = models.CharField(default="", max_length=5)
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
    superAwakenings_raw = models.TextField(default="")

    evolutions = models.ManyToManyField(Evolution)
    evos_raw = models.TextField(default="")

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

    sellMP = models.IntegerField(default=0)
    sellCoin = models.IntegerField(default=0)

    enemy_skills = models.TextField(default="")

    server = models.CharField(default='', max_length=2)

    def __str__(self):
        return self.name


class EnemySkill(models.Model):
    name = models.TextField(default="")
    effect = models.TextField(default="")
    enemy_skill_id = models.IntegerField(default=-1)
