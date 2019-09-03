from django.db import models


class Monster(models.Model):
    card_id = models.IntegerField(default=0)

    active_skill_id = models.IntegerField(blank=True, default=0)
    ancestor_id = models.IntegerField(default=0)

    attribute_id = models.IntegerField(default=0)
    attribute = models.CharField(default="", max_length=100)
    sub_attribute_id = models.IntegerField(default=0)
    sub_attribute = models.CharField(default="", max_length=100)

    awakenings = models.TextField(default="")
    super_awakenings = models.TextField(default="")

    cost = models.IntegerField(default=0)

    inheritable = models.BooleanField(default=False)
    is_collab = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    is_ult = models.BooleanField(default=False)
    leader_skill_id = models.IntegerField(blank=True, default=0)
    max_atk = models.IntegerField(default=0)
    max_hp = models.IntegerField(default=0)
    max_level = models.IntegerField(default=0)
    max_rcv = models.IntegerField(default=0)
    min_atk = models.IntegerField(default=0)
    min_hp = models.IntegerField(default=0)
    min_rcv = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=200)
    rarity = models.IntegerField(default=0)

    evolutions = models.TextField(default="")

    evo_mat_1 = models.IntegerField(default=0)
    evo_mat_2 = models.IntegerField(default=0)
    evo_mat_3 = models.IntegerField(default=0)
    evo_mat_4 = models.IntegerField(default=0)
    evo_mat_5 = models.IntegerField(default=0)

    un_evo_mat_1 = models.IntegerField(default=0)
    un_evo_mat_2 = models.IntegerField(default=0)
    un_evo_mat_3 = models.IntegerField(default=0)
    un_evo_mat_4 = models.IntegerField(default=0)
    un_evo_mat_5 = models.IntegerField(default=0)

    type_1_id = models.IntegerField(default=0)
    type_2_id = models.IntegerField(default=0)
    type_3_id = models.IntegerField(default=0)

    sell_mp = models.IntegerField(default=0)
    sell_coin = models.IntegerField(default=0)
    enemy_skills = models.TextField(default="")
    server = models.CharField(default='', max_length=2)
    collab = models.CharField(default='', max_length=50)
    collab_id = models.IntegerField(default=0)

    related_dungeons = models.TextField(default='')

    def __str__(self):
        return self.name
