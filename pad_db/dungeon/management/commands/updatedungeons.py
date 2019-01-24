from django.core.management.base import BaseCommand
import requests
import json
from ...models import Dungeon, Floor
import time
from .dParse import getModifiers
from .maps import raw7_map


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        Dungeon.objects.all().delete()
        Floor.objects.all().delete()

        start = time.time()

        link = "https://storage.googleapis.com/mirubot/paddata/processed/na_dungeons.json"

        data = requests.get(link).text
        pull = json.loads(data)

        for item in pull:
            name = item['clean_name']

            if '*' not in name:

                dungeon = Dungeon()
                dungeon.name = name.rsplit("#")[-1]
                dungeon.dungeonID = item['dungeon_id']
                dungeon.floorCount = len(item['floors'])
                dungeon.dungeonType = item['alt_dungeon_type']
                dungeon.save()

                for floorItem in item['floors']:

                    raw = floorItem['raw']

                    floor = Floor()
                    floor.dungeonID = dungeon.dungeonID
                    floor.floorNumber = raw[0]
                    floor.name = raw[1].split('$')[-1]
                    floor.battles = raw[2]
                    floor.stamina = raw[4]
                    floor.otherModifier = raw7_map[int(raw[7])]
                    pos = 8
                    possibleDrops = {}

                    while (int(raw[pos]) is not 0):
                        rawVal = int(raw[pos])
                        if rawVal > 10000:
                            val = rawVal - 10000
                            possibleDrops[val] = "rare"
                            pos += 1
                        else:
                            possibleDrops[rawVal] = "normal"
                            pos += 1
                    pos += 1
                    modifiers = getModifiers(raw, pos)

                    floor.entryRequirement = modifiers.entryRequirement
                    floor.requiredDungeon = modifiers.requiredDungeon
                    floor.modifiers = json.dumps(modifiers.modifiers)

                    floor.possibleDrops = json.dumps(possibleDrops)
                    floor.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)

