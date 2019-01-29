from django.core.management.base import BaseCommand
import requests
import json
from dungeon.models import Dungeon, Floor
import time
import os


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):

        def make_dungeon(item):
            dungeon = Dungeon()
            dungeon.name = item['clean_name'].rsplit("#")[-1]
            dungeon.dungeonID = item['dungeon_id']
            dungeon.floorCount = len(item['floors'])
            dungeon.dungeonType = item['alt_dungeon_type']
            dungeon.save()

        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        Dungeon.objects.all().delete()
        # Floor.objects.all().delete()

        start = time.time()

        with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/na_dungeons.json'), 'r') as jsonPull:
            pull = json.load(jsonPull)

            for item in pull:
                name = item['clean_name']

                if '*' not in name:
                    make_dungeon(item)

                    # for floorItem in item['floors']:
                    #     floor = Floor()
                    #     floor.dungeonID = item['dungeon_id']
                    #     floor.floorNumber = floorItem['floor_number']
                    #     floor.name = floorItem['clean_name']
                    #     floor.waves = floorItem['waves']
                    #     floor.otherModifier = floorItem['other_modifier']
                    #     floor.possibleDrops = json.dumps(floorItem['possible_drops'])
                    #     floor.entryRequirement = floorItem['entry_requirement'] if floorItem[
                    #                                                                    'entry_requirement'] is not None else "None"
                    #     floor.requiredDungeon = floorItem['required_dungeon']
                    #     floor.remainingModifiers = json.dumps(floorItem['remaining_modifiers'])
                    #     floor.modifiers = json.dumps(floorItem['stat_modifiers'])
                    #     floor.enhancedType = floorItem['enhanced_type']
                    #     floor.enhancedAttribute = floorItem['enhanced_attribute']
                    #     floor.messages = json.dumps(floorItem['messages'])
                    #     floor.fixedTeam = json.dumps(floorItem['fixed_team'])
                    #     floor.remainingModifiers = json.dumps(floorItem['remaining_modifiers'])
                    #     floor.score = floorItem['score']
                    #
                    #     floor.save()

            end = time.time()
            self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
            print("Elapsed time :", end - start)
