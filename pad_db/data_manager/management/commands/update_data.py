import json
import os

from tqdm import tqdm
from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill
from monsters.models import Monster
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

        def make_monster_data(monster_data):
            print('Building Monster database table')
            print('Deleting existing Monsters')
            Monster.objects.all().delete()
            print('Processing monsters...')
            for monster in tqdm(monster_data):
                new_monster = Monster()
                new_monster.card_id = card_id
                new_monster.name = name
                new_monster.attr_id = attr_id
                new_monster.sub_attr_id = sub_attr_id
                new_monster.is_ult = is_ult
                new_monster.type_1__id = type_1__id
                new_monster.type_2__id = type_2__id
                new_monster.rarity = rarity
                new_monster.cost = cost
                new_monster.max_level = max_level
                new_monster.feed_xp_at_lvl_4 = feed_xp_at_lvl_4
                new_monster.released_status = released_status
                new_monster.sell_price_at_lvl_10 = sell_price_at_lvl_10
                new_monster.min_hp = min_hp
                new_monster.max_hp = max_hp
                new_monster.hp_scale = hp_scale
                new_monster.min_atk = min_atk
                new_monster.max_atk = max_atk
                new_monster.atk_scale = atk_scale
                new_monster.min_rcv = min_rcv
                new_monster.max_rcv = max_rcv
                new_monster.rcv_scale = rcv_scale
                new_monster.xp_max = xp_max
                new_monster.xp_scale = xp_scale
                new_monster.active_skill_id = active_skill_id
                new_monster.leader_skill_id = leader_skill_id
                new_monster.enemy_turns = enemy_turns
                new_monster.enemy_hp_min = enemy_hp_min
                new_monster.enemy_hp_max = enemy_hp_max
                new_monster.enemy_hp_scale = enemy_hp_scale
                new_monster.enemy_atk_min = enemy_atk_min
                new_monster.enemy_atk_max = enemy_atk_max
                new_monster.enemy_atk_scale = enemy_atk_scale
                new_monster.enemy_def_min = enemy_def_min
                new_monster.enemy_def_max = enemy_def_max
                new_monster.enemy_def_scale = enemy_def_scale
                new_monster.enemy_max_level = enemy_max_level
                new_monster.enemy_coins_at_lvl_2 = enemy_coins_at_lvl_2
                new_monster.enemy_xp_at_lvl_2 = enemy_xp_at_lvl_2
                new_monster.ancestor_id = ancestor_id
                new_monster.evo_mat_id_1 = evo_mat_id_1
                new_monster.evo_mat_id_2 = evo_mat_id_2
                new_monster.evo_mat_id_3 = evo_mat_id_3
                new_monster.evo_mat_id_4 = evo_mat_id_4
                new_monster.evo_mat_id_5 = evo_mat_id_5
                new_monster.un_evo_mat_1 = un_evo_mat_1
                new_monster.un_evo_mat_2 = un_evo_mat_2
                new_monster.un_evo_mat_3 = un_evo_mat_3
                new_monster.un_evo_mat_4 = un_evo_mat_4
                new_monster.un_evo_mat_5 = un_evo_mat_5
                new_monster.enemy_turns_alt = enemy_turns_alt
                new_monster.enemy_skill_effect = enemy_skill_effect
                new_monster.enemy_skill_refs = enemy_skill_refs
                new_monster.awakenings = awakenings
                new_monster.super_awakenings = super_awakenings
                new_monster.base_id = base_id
                new_monster.type_3__id = type_3__id
                new_monster.sell_mp = sell_mp
                new_monster.latent_on_feed = latent_on_feed
                new_monster.collab_id = collab_id
                new_monster.inheritable = inheritable
                new_monster.is_collab = is_collab
                new_monster.limit_mult = limit_mult
                new_monster.voice_id = voice_id
                new_monster.evo_list = evo_list
                new_monster.server = server

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
        make_monster_data(monster_data)
