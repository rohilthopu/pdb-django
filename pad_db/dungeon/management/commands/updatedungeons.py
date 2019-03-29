from django.core.management.base import BaseCommand
import json
from dungeon.models import Dungeon, Floor, EncounterSet
from dataversions.models import Version
import time
from .dungeon_parser.dungeon_parser import get_dungeon_list
from django.conf import settings
from Utils.progress import progress


class Command(BaseCommand):
    def handle(self, *args, **options):

        def make_dungeon_from_object(dungeon, image_id, server):
            if "*" not in dungeon.clean_name:
                new_dungeon = Dungeon()
                new_dungeon.name = dungeon.clean_name
                new_dungeon.dungeonID = dungeon.dungeon_id
                new_dungeon.floorCount = len(dungeon.floors)
                new_dungeon.dungeonType = dungeon.alt_dungeon_type
                new_dungeon.imageID = image_id[0] if len(image_id) > 0 else 0
                new_dungeon.server = server
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

        def validate_card_id(card_id) -> int:
            if card_id / 100000 > 0:
                return card_id % 100000
            return card_id

        self.stdout.write('Starting dungeon update')

        start = time.time()

        prevSize = Dungeon.objects.all().count()

        Dungeon.objects.all().delete()
        Floor.objects.all().delete()

        if settings.DEBUG:
            self.stdout.write('\tDebug option enabled')
            self.stdout.write('\tGrabbing files from alternative locations')
            location = '/Users/rohil/projects/personal/data_files/raw/na/download_dungeon_data.json'
            location2 = '/Users/rohil/projects/personal/data_files/raw/jp/download_dungeon_data.json'
        else:
            self.stdout.write('\tUsing standard file path')
            location = '/home/rohil/data/pad_data/raw_data/na/download_dungeon_data.json'
            location2 = '/home/rohil/data/pad_data/raw_data/jp/download_dungeon_data.json'
        self.stdout.write('\tLocation 1, NA: {}'.format(location))
        self.stdout.write('\tLocation 2, JP: {}'.format(location2))

        self.stdout.write('Building NA dungeon list...')
        na_dungeon_list = get_dungeon_list(location)
        self.stdout.write('Build complete.')
        self.stdout.write('Building initial NA database...')

        total = len(na_dungeon_list)

        for i in range(0, total):
            item = na_dungeon_list[i]
            progress(i, total)
            make_dungeon_from_object(item, [*item.floors[-1].possible_drops], 'na')
            if '*' not in item.clean_name:
                make_floor_from_object(item.floors, item.dungeon_id)

        print()

        self.stdout.write('NA conversion complete.')

        self.stdout.write('Building JP dungeon list...')
        jp_dungeon_list = get_dungeon_list(location2)
        self.stdout.write('Build complete.')
        self.stdout.write('Merging in JP dungeons...')
        total = len(jp_dungeon_list)
        for i in range(0, total):
            item = jp_dungeon_list[i]
            progress(i, total)
            if not Dungeon.objects.filter(dungeonID=item.dungeon_id).exists():
                make_dungeon_from_object(item, [*item.floors[-1].possible_drops], 'jp')
                make_floor_from_object(item.floors, item.dungeon_id)
        print()
        self.stdout.write('Merge complete.')

        encounters = EncounterSet.objects.all()
        dungeons = Dungeon.objects.all()
        floors = Floor.objects.all()

        self.stdout.write('Linking dungeon images.')

        total = dungeons.count()

        for i in range(0, total):
            dungeon = dungeons[i]
            progress(i, total)
            encounter_data = encounters.filter(dungeon_id=dungeon.dungeonID)
            dungeon_floors = floors.filter(dungeonID=dungeon.dungeonID)

            if encounter_data.last() is not None:
                boss = encounter_data.last().encounter_data

                card_id = json.loads(boss)[-1]['card_id']
                dungeon.imageID = validate_card_id(card_id)
                dungeon.save()

                for floor in dungeon_floors:
                    boss = encounter_data.filter(floor_id=floor.floorNumber)
                    if boss is not None and boss.last() is not None:
                        card_id = json.loads(boss.last().encounter_data)[-1]['card_id']
                        floor.imageID = validate_card_id(card_id)
                        floor.save()

        end = time.time()

        print()
        self.stdout.write("Elapsed time : {}".format(end - start))

        self.stdout.write("Updating version")

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

        self.stdout.write('Dungeon database build complete.')
