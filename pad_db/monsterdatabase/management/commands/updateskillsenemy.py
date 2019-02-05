from django.core.management.base import BaseCommand, CommandError
from monsterdatabase.models import EnemySkill

import json
import time
import os


class Command(BaseCommand):
    help = 'Runs an update on the models to add to the database.'

    def handle(self, *args, **options):

        def makeSkill(item):

            skill = EnemySkill()
            skill.enemy_skill_id = item['enemy_skill_id']

            name = item['name']
            clean_name = name.replace('\n', ' ') if name is not None else name

            effect = str(item['params'][0])

            clean_effect = effect.replace('\n', ' ') if effect is not None else effect

            skill.name = clean_name
            skill.effect = clean_effect if clean_effect is not None else "No Effect"

            skill.save()

        s = EnemySkill.objects.all().delete()

        with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/na_enemy_skills.json'), 'r') as jsonPull:
            s.delete()
            jsonData = json.load(jsonPull)

            print()
            print("Updating NA enemy skill list.")
            print()
            start = time.time()

            for item in jsonData:

                name = item['name']
                if '無し' not in name and name is not '' and '*' not in name:
                    makeSkill(item)

        with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/jp_enemy_skills.json'), 'r') as jsonPull:
            jsonData = json.load(jsonPull)
            print()
            print("Merging JP enemy skill list.")
            print()

            currSkills = EnemySkill.objects.all()

            for item in jsonData:
                enemy_skill_id = item['enemy_skill_id']
                if enemy_skill_id != 0 and not currSkills.filter(enemy_skill_id=enemy_skill_id).exists():
                    makeSkill(item)

            end = time.time()
            print()
            print("Elapsed time:", end - start, "s")
            print()
