from django.core.management.base import BaseCommand
import requests
import json
from ...models import Dungeon
import time


class Command(BaseCommand):
    help = 'Clears the daily dungeon list.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting NA DUNGEON DB update.'))


        for dun in Dungeon.objects.all():
            dun.delete()


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
                dungeon.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('NA DUNGEON update complete.'))
        print("Elapsed time :", end - start)
