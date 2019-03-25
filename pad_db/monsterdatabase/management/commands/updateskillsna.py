from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import Skill
from dataversions.models import Version
import json
import time
import os
from .monster_skill import MonsterSkill
from .skill_type_maps import SKILL_TYPE


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        def makeSkill(item):

            skill = Skill()
            skill.name = item.name
            skill.description = item.clean_description
            skill.skillID = item.skill_id

            if item.levels is not None:
                skill.levels = item.levels
                skill.maxTurns = item.turn_max
                skill.minTurns = item.turn_min
                skill.skill_type = "active"
            else:
                skill.skill_type = "leader"

            skill_type = item.skill_type
            skill.skill_class = SKILL_TYPE[skill_type]

            skill.hp_mult = item.hp_mult
            skill.atk_mult = item.atk_mult
            skill.rcv_mult = item.rcv_mult
            skill.dmg_reduction = item.shield / 100

            c_skill_1 = item.skill_part_1_id
            c_skill_2 = item.skill_part_2_id
            c_skill_3 = item.skill_part_3_id

            if c_skill_1 is not None:
                skill.c_skill_1 = c_skill_1
            if c_skill_2 is not None:
                skill.c_skill_2 = c_skill_2
            if c_skill_3 is not None:
                skill.c_skill_3 = c_skill_3

            skill.save()

        s = Skill.objects.all()
        prevSize = s.count()

        with open(os.path.abspath('/home/rohil/data/pad_data/raw_data/na/download_skill_data.json'), 'r') as jsonPull:
            s.delete()
            jsonData = json.load(jsonPull)

            print()
            print("Updating NA skill list.")
            print()
            start = time.time()

            for i, ms in enumerate(jsonData['skill']):

                try:
                    parsed_skill = MonsterSkill(i, ms)

                    if '無し' not in parsed_skill.name and '*' not in parsed_skill.name and parsed_skill.skill_id != 0:
                        makeSkill(parsed_skill)
                except:
                    print('Error at', i)
                    print('Data', ms)
                    print()

        with open(os.path.abspath('/home/rohil/data/pad_data/raw_data/jp/download_skill_data.json'), 'r') as jsonPull:
            jsonData = json.load(jsonPull)
            print()
            print("Merging JP skill list.")
            print()

            currSkills = Skill.objects.all()

            for i, ms in enumerate(jsonData['skill']):
                try:
                    parsed_skill = MonsterSkill(i, ms)

                    if parsed_skill.skill_id != 0 and not currSkills.filter(
                            skillID=parsed_skill.skill_id).exists() and parsed_skill.skill_id != 0:
                        makeSkill(parsed_skill)
                except:
                    print('Error at', i)
                    print('Data', ms)
                    print()
            end = time.time()
            print()
            print("Elapsed time:", end - start, "s")
            print()

        print()
        print("Updating version")

        ver = Version.objects.all()

        if len(ver) == 0:
            v = Version()
            v.monster = 1
            v.save()
        else:
            v = ver.first()
            if prevSize < Skill.objects.all().count():
                v.monster += 1
            v.save()
