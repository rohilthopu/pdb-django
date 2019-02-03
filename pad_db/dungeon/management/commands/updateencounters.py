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

        Encounter.objects.all().delete()

        with open(os.path.abspath('/home/rohil/data/pad_data/padguide/etlDungeonMap.json'), 'r') as jsonData:
            map_data = json.load(jsonData)

        dungeon_map = {}

        for item in map_data['items']:
            dungeon_map[int(item['DUNGEON_SEQ'])] = int(item['PAD_DUNGEON_ID'])

        with open(os.path.abspath('/home/rohil/data/pad_data/padguide/dungeonMonsterList.json'), 'r') as jsonData:
            encounter_data = json.load(jsonData)

        for item in encounter_data['items']:

            if int(item['DUNGEON_SEQ']) in dungeon_map.keys():

                try:
                    dungeon_id = dungeon_map[int(item['DUNGEON_SEQ'])]
                    turn = int(item['TURN'])
                    wave = int(item['FLOOR'])
                    floor = int(item['ORDER_IDX'])
                    monster_id = int(item['MONSTER_NO'])
                    hp = int(item['HP'])
                    atk = int(item['ATK'])
                    defense = float(item['DEF'])
                    drop_id = int(item['DROP_NO'])
                    comment = item['COMMENT_US']

                    encounter = Encounter()
                    encounter.wave = wave
                    encounter.floor = floor
                    encounter.turn = turn
                    encounter.monster_id = monster_id
                    encounter.hp = hp
                    encounter.atk = atk
                    encounter.defense = defense
                    encounter.drop_id = drop_id
                    encounter.dungeon_id = dungeon_id
                    encounter.comment = comment
                    encounter.save()
                except Exception as e:
                    print("Error saving data with exception", e)
                    print("Data:", item)
                    print()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)
