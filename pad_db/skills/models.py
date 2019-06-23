from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField(default="", blank=True, )
    skill_id = models.IntegerField(default=-1)
    skill_type = models.CharField(max_length=50, default="")
    hp_mult = models.FloatField(default=1)
    atk_mult = models.FloatField(default=1)
    rcv_mult = models.FloatField(default=1)
    dmg_reduction = models.FloatField(default=0)

    # connected skills
    skill_part_1_id = models.IntegerField(default=-1)
    skill_part_2_id = models.IntegerField(default=-1)
    skill_part_3_id = models.IntegerField(default=-1)

    # skill type
    skill_class = models.CharField(max_length=100, default="")

    levels = models.IntegerField(default=0)
    max_turns = models.IntegerField(blank=True, default=0)
    min_turns = models.IntegerField(blank=True, default=0)
    server = models.CharField(default='', max_length=2)
