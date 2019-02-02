from django.core.management.base import BaseCommand
import json
from dungeon.models import Encounter
import time
import os
from .dungeon_parser.dungeon_parser import get_dungeon_list


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Starting Dungeon encounter build.'))

        start = time.time()

        with open(os.path.abspath('/home/rohil/data/pad_data/padguide/etlDungeonMap.json'), 'r') as jsonData:
            map_data = json.load(jsonData)

        dungeon_map = {}

        for item in map_data['items']:
            dungeon_map[int(item['DUNGEON_SEQ'])] = int(item['PAD_DUNGEON_ID'])

        with open(os.path.abspath('/home/rohil/data/pad_data/padguide/dungeonMonsterList.json'), 'r') as jsonData:
            encounter_data = json.load(jsonData)

        for item in encounter_data['items']:
            wave = int(item['TURN'])
            floor = int(item['FLOOR'])
            monster_id = int(item['MONSTER_NO'])
            hp = int(item['HP'])
            atk = int(item['ATK'])
            defense = int(item['DEF'])
            drop_id = int(item['DROP_NO'])
            dungeon_id = dungeon_map[int(item['DUNGEON_SEQ'])]
            comment = item['COMMENT_US']

            encounter = Encounter()
            encounter.wave = wave
            encounter.floor = floor
            encounter.monster_id = monster_id
            encounter.hp = hp
            encounter.atk = atk
            encounter.defense = defense
            encounter.drop_id = drop_id
            encounter.dungeon_id = dungeon_map
            encounter.comment = comment
            encounter.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)
