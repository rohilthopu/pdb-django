import json
import os

from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill
from monsters.models import Monster
from dungeons.models import Dungeon, Floor
from pad_db.settings import DEBUG

DEVELOPMENT_PATH = '/Users/rohil/projects/personal/pdb_processor/output'
PRODUCTION_PATH = '/home/rohil/pdb-processor/output'
SKILLS_FILE_NAME = 'skills.json'
MONSTERS_FILE_NAME = 'monsters.json'
DUNGEONS_FILE_NAME = 'dungeons.json'


@transaction.atomic
class Command(BaseCommand):
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
                new_skill.levels = skill['levels']
                new_skill.shield = skill['shield']
                new_skill.server = skill['server']
                new_skill.save()
            print("Skill database build complete!")

        def make_monster_data(monster_data):
            print('Building Monster database table')
            print('Deleting existing Monsters')
            Monster.objects.all().delete()
            print('Processing monsters...')
            for monster in tqdm(monster_data):
                new_monster = Monster()
                new_monster.card_id = monster['card_id']
                new_monster.name = monster['name']
                new_monster.attr_id = monster['attr_id']
                new_monster.sub_attr_id = monster['sub_attr_id']
                new_monster.is_ult = monster['is_ult']
                new_monster.type_1 = monster['type_1_id']
                new_monster.type_2 = monster['type_2_id']
                new_monster.rarity = monster['rarity']
                new_monster.cost = monster['cost']
                new_monster.max_level = monster['max_level']
                new_monster.feed_xp_at_lvl_4 = monster['feed_xp_at_lvl_4']
                new_monster.released_status = monster['released_status']
                new_monster.sell_price_at_lvl_10 = monster['sell_price_at_lvl_10']
                new_monster.min_hp = monster['min_hp']
                new_monster.max_hp = monster['max_hp']
                new_monster.min_atk = monster['min_atk']
                new_monster.max_atk = monster['max_atk']
                new_monster.min_rcv = monster['min_rcv']
                new_monster.max_rcv = monster['max_rcv']
                new_monster.xp_max = monster['xp_max']
                new_monster.active_skill_id = monster['active_skill_id']
                new_monster.leader_skill_id = monster['leader_skill_id']
                new_monster.enemy_turns = monster['enemy_turns']
                new_monster.enemy_hp_min = monster['enemy_hp_min']
                new_monster.enemy_hp_max = monster['enemy_hp_max']
                new_monster.enemy_atk_min = monster['enemy_atk_min']
                new_monster.enemy_atk_max = monster['enemy_atk_max']
                new_monster.enemy_def_min = monster['enemy_def_min']
                new_monster.enemy_def_max = monster['enemy_def_max']
                new_monster.enemy_max_level = monster['enemy_max_level']
                new_monster.ancestor_id = monster['ancestor_id']
                new_monster.evo_mat_id_1 = monster['evo_mat_id_1']
                new_monster.evo_mat_id_2 = monster['evo_mat_id_2']
                new_monster.evo_mat_id_3 = monster['evo_mat_id_3']
                new_monster.evo_mat_id_4 = monster['evo_mat_id_4']
                new_monster.evo_mat_id_5 = monster['evo_mat_id_5']
                new_monster.un_evo_mat_1 = monster['un_evo_mat_1']
                new_monster.un_evo_mat_2 = monster['un_evo_mat_2']
                new_monster.un_evo_mat_3 = monster['un_evo_mat_3']
                new_monster.un_evo_mat_4 = monster['un_evo_mat_4']
                new_monster.un_evo_mat_5 = monster['un_evo_mat_5']
                new_monster.enemy_turns_alt = monster['enemy_turns_alt']
                new_monster.enemy_skill_effect = monster['enemy_skill_effect']
                new_monster.enemy_skill_refs = monster['enemy_skill_refs']
                new_monster.awakenings = monster['awakenings']
                new_monster.super_awakenings = monster['super_awakenings']
                new_monster.type_3= monster['type_3_id']
                new_monster.sell_mp = monster['sell_mp']
                new_monster.collab_id = monster['collab_id']
                new_monster.inheritable = monster['inheritable']
                new_monster.is_collab = monster['is_collab']
                new_monster.limit_mult = monster['limit_mult']
                new_monster.evolutions = monster['evo_list']
                new_monster.server = monster['server']
                new_monster.save()
            print('Monster database build complete!')

        def make_dungeon_from_object(dungeons):
            print('Building Dungeon database table')
            print('Deleting existing Dungeon')
            Dungeon.objects.all().delete()
            print('Processing dungeon...')
            for dungeon in tqdm(dungeons):
                new_dungeon = Dungeon()
                new_dungeon.name = dungeon['clean_name']
                new_dungeon.dungeon_id = dungeon['dungeon_id']
                new_dungeon.floor_count = len(dungeon['floors'])
                new_dungeon.dungeon_type = dungeon['alt_dungeon_type']
                new_dungeon.image_id = dungeon['image_id']
                new_dungeon.server = dungeon['server']
                new_dungeon.save()
                make_floor_from_object(dungeon['floors'])

        def make_floor_from_object(floors):
            # print('Building Floors database table')
            # print('Deleting existing Floors')
            Floor.objects.all().delete()
            # print('Processing floors...')
            for floor in floors:
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
                fl.save()

        if DEBUG:
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)
            with open(os.path.abspath('{}/{}'.format(DEVELOPMENT_PATH, DUNGEONS_FILE_NAME)), 'r') as dungeon_file:
                dungeon_data = json.load(dungeon_file)

        else:
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, SKILLS_FILE_NAME)), 'r') as skill_file:
                skill_data = json.load(skill_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, MONSTERS_FILE_NAME)), 'r') as monster_file:
                monster_data = json.load(monster_file)
            with open(os.path.abspath('{}/{}'.format(PRODUCTION_PATH, DUNGEONS_FILE_NAME)), 'r') as dungeon_file:
                dungeon_data = json.load(dungeon_file)

        make_skill_data(skill_data)
        make_monster_data(monster_data)
        make_dungeon_from_object(dungeon_data)
        print()
