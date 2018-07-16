from django.core.management.base import BaseCommand
import requests
import json

from guerrilladungeon.models import GuerrillaDungeon


class Command(BaseCommand):
    help = "Updates the Guerrilla Dungeon List."

    def handle(self, *args, **options):

        link = "https://storage.googleapis.com/mirubot/paddata/merged/guerrilla_data.json"
        jsonPull = requests.get(link).text
        jsonDump = json.loads(jsonPull)



        # for d in GuerrillaDungeon.objects.all():
        #     d.delete()


        for item in jsonDump['items']:

            if GuerrillaDungeon.objects.filter(startTime=item['start_timestamp']).first() is None:
                dungeon = GuerrillaDungeon()

                dungeon.name = item['dungeon_name']
                dungeon.startTime = item['start_timestamp']
                dungeon.endTime = item['end_timestamp']
                dungeon.group = item['group']
                dungeon.server = item['server']
                dungeon.save()

        for d in GuerrillaDungeon.objects.all():
            print(d.name, d.server, d.group)
