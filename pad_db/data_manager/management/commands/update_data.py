import json
import os

from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill
from pad_db.settings import DEBUG

DEVELOPMENT_PATH = '/Users/rohil/projects/personal/pdb_processor/output'
PRODUCTION_PATH = '/home/rohil/pdb-processor/output'
SKILLS_FILE_NAME = 'skills.json'
MONSTERS_FILE_NAME = 'monsters.json'
DUNGEONS_FILE_NAME = 'dungeons.json'


@transaction.atomic
class Command(BaseCommand):
    help = "Updates the Guerrilla Dungeon List."

    def handle(self, *args, **options):
        def make_skill_data(skill_data):
            print('Building Skills database table')
            print('Deleting existing Skills')
            Skill.objects.all().delete()
            print('Processing skills...')
            for skill in tqdm(skill_data):
                new_skill = Skill()
                new_skill.skill_id = skill['skill_id']
                new_skill.name = skill['name']
                new_skill.description = skill['description']
                new_skill.skill_part_1_id = skill['skill_part_1_id']
                new_skill.skill_part_2_id = skill['skill_part_2_id']
                new_skill.skill_part_3_id = skill['skill_part_3_id']
                new_skill.max_turns = skill['max_turns']
                new_skill.min_turns = skill['min_turns']
                new_skill.hp_mult = skill['hp_mult']
                new_skill.atk_mult = skill['atk_mult']
                new_skill.rcv_mult = skill['rcv_mult']
                new_skill.shield = skill['shield']
                new_skill.server = skill['server']
                new_skill.save()
            print("Skill database build complete!")

        if DEBUG:
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)


        else:
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)
        make_skill_data(skill_data)
