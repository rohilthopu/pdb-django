from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import EnemySkill
from enemy_skill_parser import parse_enemy_skills
import json
import time
import os


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        EnemySkill.objects.all().delete()

        def makeSkill(item):

            skill = EnemySkill()
            skill.enemy_skill_id = item.skill_id
            # name = item['name']
            # clean_name = name.replace('\n', ' ') if name is not None else name
            #
            # effect = str(item['params'][0])
            #
            # clean_effect = effect.replace('\n', ' ') if effect is not None else effect

            skill.name = item.name
            skill.effect = item.effect

            skill.save()

        with open(os.path.abspath('/home/rohil/data/pad_data/raw_data/na/download_enemy_skill_data.json'),
                  'r') as jsonPull:
            jsonData = json.load(jsonPull)

            print()
            print("Updating NA enemy skill list.")
            print()
            start = time.time()

            parsed_skills = parse_enemy_skills(jsonData)

            for skill in parsed_skills:
                makeSkill(skill)

        with open(os.path.abspath('/home/rohil/data/pad_data/raw_data/jp/download_enemy_skill_data.json'),
                  'r') as jsonPull:
            jsonData = json.load(jsonPull)
            print()
            print("Merging JP enemy skill list.")
            print()

            currSkills = EnemySkill.objects.all()

            parsed_skills = parse_enemy_skills(jsonData)

            for skill in parsed_skills:
                enemy_skill_id = skill.skill_id
                if enemy_skill_id != 0 and not currSkills.filter(enemy_skill_id=enemy_skill_id).exists():
                    makeSkill(skill)

            end = time.time()
            print()
            print("Elapsed time:", end - start, "s")
            print()
