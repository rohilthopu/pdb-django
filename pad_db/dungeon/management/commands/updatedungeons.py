from django.core.management.base import BaseCommand
import requests
import json
from dungeon.models import Dungeon, Floor
import time
import os
from .dungeon_parser.dungeon_parser import get_dungeon_list


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

        def make_dungeon_from_object(dungeon):
            item = Dungeon()
            dungeon.name = dungeon.clean_name
            dungeon.dungeonID = dungeon.dungeon_id
            dungeon.floorCount = len(dungeon.floors)
            dungeon.dungeonType = dungeon.alt_dungeon_type
            item.save()

        def make_floor_from_object(floors, dungeon_id):

            for floor in floors:
                fl = Floor()
                fl.dungeonID = dungeon_id
                fl.floorNumber = floor.floor_number
                fl.name = floor.clean_name
                fl.waves = floor.waves
                fl.possibleDrops = json.dumps(floor.possible_drops)
                fl.entryRequirement = floor.entry_requirement if floor.entry_requirement is not None else "None"
                fl.requiredDungeon = floor.required_dungeon if floor.required_dungeon is not None else "None"
                fl.remainingModifiers = json.dumps(floor.remaining_modifiers)
                fl.teamModifiers = json.dumps(floor.team_modifiers)
                fl.encounterModifiers = json.dumps(floor.modifiers_clean)

                fl.enhancedType = floor.enhanced_type if floor.enhanced_type is not None else "None"
                fl.enhancedAttribute = floor.enhanced_attribute if floor.enhanced_attribute is not None else "None"
                fl.messages = json.dumps(floor.messages)
                fl.fixedTeam = json.dumps(floor.fixed_team)
                fl.score = floor.score if floor.score is not None else 0
                fl.save()

        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        start = time.time()

        Dungeon.objects.all().delete()
        Floor.objects.all().delete()

        dungeon_list = get_dungeon_list()

        for item in dungeon_list:

            make_dungeon_from_object(item)

            make_floor_from_object(item.floors, item.dungeon_id)



        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)
