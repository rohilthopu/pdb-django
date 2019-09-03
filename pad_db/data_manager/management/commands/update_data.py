import json
import os

from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill
from monsters.models import Monster
from dungeons.models import Dungeon, Floor
from pad_db.settings import DEBUG
from guerrilla.models import GuerrillaDungeon

try:
    DEVELOPMENT_PATH = os.environ['pdb_processor_output']
except:
    DEVELOPMENT_PATH = '/Users/rohil/projects/personal/pdb-processor/data/output'

PRODUCTION_PATH = '/home/pdb-processor/data/output'
SKILLS_FILE_NAME = 'skills.json'
MONSTERS_FILE_NAME = 'monsters.json'
DUNGEONS_FILE_NAME = 'dungeons.json'
GUERRILLA_FILE_NAME = 'guerrilla_data.json'


@transaction.atomic
class Command(BaseCommand):
    def handle(self, *args, **options):

        def make_guerrilla_data(guerrilla_data):
            gds = []
            print('Building Guerrilla database table')
            print('Processing guerrilla dungeons...')
            for item in tqdm(guerrilla_data):
                dungeon = GuerrillaDungeon()
                dungeon.name = item['name']
                dungeon.start_time = item['start_time']
                dungeon.end_time = item['end_time']
                dungeon.start_secs = item['start_secs']
                dungeon.end_secs = item['end_secs']
                dungeon.group = item['group']
                dungeon.server = item['server']
                dungeon.dungeon_id = item['dungeon_id']
                dungeon.image_id = item['image_id']
                dungeon.status = item['status']
                gds.append(dungeon)
            print('Deleting existing Guerrilla Dungeons')
            GuerrillaDungeon.objects.all().delete()
            print('Inserting Guerrilla Dungeons')
            GuerrillaDungeon.objects.bulk_create(gds)
            print("Guerrilla Dungeon database build complete!")

        def make_skill_data(skill_data):
            skills = []
            print('Building Skills database table')
            print('Processing skills...')
            for skill in tqdm(skill_data):
                new_skill = Skill()
                for key, val in skill.items():
                    setattr(new_skill, key, val)
                skills.append(new_skill)
            print('Deleting existing Skills')
            Skill.objects.all().delete()
            print('Inserting Skills')
            Skill.objects.bulk_create(skills)
            print("Skill database build complete!")

        def make_monster_data(monster_data):
            print('Building Monster database table')
            monsters = []
            print('Processing monsters...')
            for monster in tqdm(monster_data):
                new_monster = Monster()

                for key, val in monster.items():

                    if type(val) == list:
                        setattr(new_monster, key, json.dumps(val))
                    else:
                        setattr(new_monster, key, val)

                monsters.append(new_monster)
            print('Deleting existing Monsters')
            Monster.objects.all().delete()
            print('Inserting monster data')
            Monster.objects.bulk_create(monsters)
            print('Monster database build complete!')

        def make_dungeon_from_object(dungeon_data):
            print('Building Dungeon database table')
            dungeons = []
            floors = []
            print('Processing dungeon...')
            for dungeon in tqdm(dungeon_data):
                new_dungeon = Dungeon()
                new_dungeon.name = dungeon['clean_name']
                new_dungeon.dungeon_id = dungeon['dungeon_id']
                new_dungeon.floor_count = len(dungeon['floors'])
                # new_dungeon.dungeon_type = dungeon['dungeon_type']
                new_dungeon.dungeon_type = ""
                new_dungeon.image_id = dungeon['image_id']
                new_dungeon.server = dungeon['server']
                dungeons.append(new_dungeon)
                make_floor_from_object(dungeon['floors'], floors)
            print('Deleting existing Dungeon data')
            Dungeon.objects.all().delete()
            Floor.objects.all().delete()
            print('Inserting Dungeon data')
            Dungeon.objects.bulk_create(dungeons)
            Floor.objects.bulk_create(floors)
            print('Dungeon database build complete!')

        def make_floor_from_object(floor_data, floors):

            for floor in floor_data:
                fl = Floor()
                fl.dungeon_id = floor['dungeon_id']
                fl.floor_number = floor['floor_number']
                fl.name = floor['clean_name']
                fl.stamina = floor['stamina']
                fl.waves = floor['waves']
                fl.possible_drops = json.dumps(floor['possible_drops'])
                fl.required_dungeon = floor['required_dungeon']
                fl.required_floor = floor['required_floor']
                fl.team_modifiers = json.dumps(floor['team_modifiers'])
                fl.encounter_modifiers = json.dumps(floor['modifiers_clean'])
                fl.enhanced_type = floor['enhanced_type']
                fl.enhanced_attribute = floor['enhanced_attribute']
                fl.messages = json.dumps(floor['messages'])
                fl.fixed_team = json.dumps(floor['fixed_team'])
                fl.score = floor['score']
                fl.image_id = floor['image_id']
                fl.wave_data = json.dumps(floor['wave_data'])
                floors.append(fl)

        if DEBUG:
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, DUNGEONS_FILE_NAME)), 'r') as dungeon_file:
                dungeon_data = json.load(dungeon_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, GUERRILLA_FILE_NAME)), 'r') as guerrilla_file:
                guerrilla_data = json.load(guerrilla_file)

        else:
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, DUNGEONS_FILE_NAME)), 'r') as dungeon_file:
                dungeon_data = json.load(dungeon_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, GUERRILLA_FILE_NAME)), 'r') as guerrilla_file:
                guerrilla_data = json.load(guerrilla_file)

        make_guerrilla_data(guerrilla_data)
        make_skill_data(skill_data)
        make_monster_data(monster_data)
        make_dungeon_from_object(dungeon_data)
        print()
