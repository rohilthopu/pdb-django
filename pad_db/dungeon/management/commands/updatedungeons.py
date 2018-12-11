from django.core.management.base import BaseCommand
import requests
import json
from ...models import Dungeon
import time


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))

        Dungeon.objects.all().delete()

        start = time.time()

        link = "https://storage.googleapis.com/mirubot/paddata/processed/na_dungeons.json"

        data = requests.get(link).text
        pull = json.loads(data)

        for item in pull:
            name = item['clean_name']

            if '*' not in name:

                for floor in item['floors']:

                    dungeon = Dungeon()

                    dungeon.name = name.rsplit("#")[-1]
                    dungeon.dungeonID = item['dungeon_id']
                    dungeon.floorCount = floor['raw'][2]
                    raw = floor['raw']

                    dungeon.floorName = raw[1]
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

                    dungeon.possibleDrops = json.dumps(possibleDrops)
                    dungeon.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)

        print("Printing all dungeon information.")

        for dungeon in Dungeon.objects.all():
            print("\tDungeon Name:", dungeon.name)
            print("\t\tFloor Name:", dungeon.floorName)
            print("\t\t\tDungeon Floor Count:", dungeon.floorCount)
            print("\t\t\tPossible Drops:", json.loads(dungeon.possibleDrops))
