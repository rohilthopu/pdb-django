from django.core.management.base import BaseCommand
import json
from dungeon.models import Dungeon, Floor
from dataversions.models import Version
import time
from .dungeon_parser.dungeon_parser import get_dungeon_list


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):

        def make_dungeon_from_object(dungeon, image_id):
            if "*" not in dungeon.clean_name:
                new_dungeon = Dungeon()
                new_dungeon.name = dungeon.clean_name
                new_dungeon.dungeonID = dungeon.dungeon_id
                new_dungeon.floorCount = len(dungeon.floors)
                new_dungeon.dungeonType = dungeon.alt_dungeon_type
                new_dungeon.imageID = image_id[0] if len(image_id) > 0 else 0
                new_dungeon.save()

        def make_floor_from_object(floors, dungeon_id):

            for floor in floors:
                fl = Floor()
                fl.dungeonID = dungeon_id
                fl.floorNumber = floor.floor_number
                fl.name = floor.clean_name
                fl.stamina = floor.stamina
                fl.waves = floor.waves
                fl.possibleDrops = json.dumps(floor.possible_drops)
                fl.requiredDungeon = floor.required_dungeon if floor.required_dungeon is not None else 0
                fl.requiredFloor = floor.required_floor if floor.required_floor is not None else 0
                fl.remainingModifiers = json.dumps(floor.remaining_modifiers)
                fl.teamModifiers = json.dumps(floor.team_modifiers)
                fl.encounterModifiers = json.dumps(floor.modifiers_clean)

                fl.enhancedType = floor.enhanced_type if floor.enhanced_type is not None else "None"
                fl.enhancedAttribute = floor.enhanced_attribute if floor.enhanced_attribute is not None else "None"
                fl.messages = json.dumps(floor.messages)
                fl.fixedTeam = json.dumps(floor.fixed_team)
                fl.score = floor.score if floor.score is not None else 0

                # Just use the last drop for the image id for now.
                image_id = [*floor.possible_drops]
                fl.imageID = image_id[0] if len(image_id) > 0 else 0
                fl.save()

        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        start = time.time()

        prevSize = Dungeon.objects.all().count()

        Dungeon.objects.all().delete()
        Floor.objects.all().delete()

        dungeon_list = get_dungeon_list()

        for item in dungeon_list:

            make_dungeon_from_object(item, [*item.floors[-1].possible_drops])

            if '*' not in item.clean_name:
                make_floor_from_object(item.floors, item.dungeon_id)

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)

        print("Updating version")

        ver = Version.objects.all()

        if len(ver) == 0:
            v = Version()
            v.monster = 1
            v.save()
        else:
            v = ver.first()
            if prevSize < Dungeon.objects.all().count():
                v.monster += 1
            v.save()
