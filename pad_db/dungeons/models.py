from django.db import models


class Floor(models.Model):
    floor_number = models.IntegerField(default=0)
    name = models.CharField(default="", max_length=100)
    stamina = models.IntegerField(default=0)
    waves = models.IntegerField(default=0)
    possible_drops = models.TextField(default="")
    dungeon_id = models.IntegerField(default=0)
    required_dungeon = models.IntegerField(default=0)
    required_floor = models.IntegerField(default=0)
    encounter_modifiers = models.TextField(default="")
    team_modifiers = models.TextField(default="")
    entry_requirement = models.TextField(default="")
    other_modifier = models.TextField(default="")
    messages = models.TextField(default="")
    score = models.IntegerField(default=0)
    fixedTeam = models.TextField(default="")
    remaining_modifiers = models.TextField(default="")
    enhanced_type = models.CharField(default=0, max_length=100)
    enhanced_attribute = models.CharField(default=0, max_length=100)
    image_id = models.IntegerField(default=0)
    wave_data = models.TextField(default="")


class Dungeon(models.Model):
    name = models.CharField(default="", max_length=100)
    dungeon_id = models.IntegerField(default=0)
    dungeon_type = models.CharField(default="", max_length=50)
    floor_count = models.IntegerField(default=0)
    image_id = models.IntegerField(default=0)
    server = models.CharField(default='', max_length=2)
