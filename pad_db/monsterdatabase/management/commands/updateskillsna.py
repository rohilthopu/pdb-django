from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import Skill
import requests
import json
import time

from .skill_parser import parse_skill_multiplier
from .skill_type_maps import SKILL_TYPE


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        def makeSkill(item):

            skill = Skill()
            skill.name = item['name']
            skill.description = item['clean_description']
            skill.skillID = item['skill_id']

            if item['levels'] is not None:
                skill.levels = item['levels']
                skill.maxTurns = item['turn_max']
                skill.minTurns = item['turn_min']
                skill.skill_type = "active"
            else:
                skill.skill_type = "leader"

            skill_type = item['skill_type']
            skill.skill_class = SKILL_TYPE[skill_type]

            skill.hp_mult = item['hp_mult']
            skill.atk_mult = item['atk_mult']
            skill.rcv_mult = item['rcv_mult']
            skill.dmg_reduction = item['shield']/100

            c_skill_1 = item['skill_part_1_id']
            c_skill_2 = item['skill_part_2_id']
            c_skill_3 = item['skill_part_3_id']

            if c_skill_1 is not None:
                skill.c_skill_1 = c_skill_1
            if c_skill_2 is not None:
                skill.c_skill_2 = c_skill_2
            if c_skill_3 is not None:
                skill.c_skill_3 = c_skill_3

            skill.save()

        # allSkills = Skill.objects.all()
        Skill.objects.all().delete()
        link = "https://storage.googleapis.com/mirubot-data/paddata/processed/na_skills.json"
        linkJP = "https://storage.googleapis.com/mirubot-data/paddata/processed/jp_skills.json"

        req = requests.get(link).text
        data = json.loads(req)

        print()
        print("Updating NA skill list.")
        print()
        start = time.time()

        for item in data:
            if item['skill_id'] != 0:
                makeSkill(item)

        print()
        print("Merging JP skill list.")
        print()

        currSkills = Skill.objects.all()

        req = requests.get(linkJP).text
        data = json.loads(req)

        for item in data:
            skillID = item['skill_id']
            if skillID != 0 and not currSkills.filter(skillID=skillID):
                makeSkill(item)

        end = time.time()
        print()
        print("Elapsed time:", end - start, "s")
        print()
