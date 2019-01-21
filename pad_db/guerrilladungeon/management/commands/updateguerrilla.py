from django.core.management.base import BaseCommand
import requests
import json
import time
from datetime import datetime

from guerrilladungeon.models import GuerrillaDungeon
from dungeon.models import Dungeon


class Command(BaseCommand):
    help = "Updates the Guerrilla Dungeon List."

    def handle(self, *args, **options):

        link = "https://storage.googleapis.com/mirubot-data/paddata/merged/guerrilla_data.json"
        jsonPull = requests.get(link).text
        jsonDump = json.loads(jsonPull)

        GuerrillaDungeon.objects.all().delete()

        for item in jsonDump['items']:

            if GuerrillaDungeon.objects.filter(startTime=item['start_timestamp']).first() is None:
                dungeon = GuerrillaDungeon()

                dungeon.name = item['dungeon_name'].rsplit('$')[-1]
                dungeon.startTime = datetime.fromtimestamp(item['start_timestamp']).strftime("%A, %B %d, %Y %H:%M")
                dungeon.endTime = datetime.fromtimestamp(item['end_timestamp']).strftime("%A, %B %d, %Y %H:%M")
                dungeon.startSecs = item['start_timestamp']
                dungeon.endSecs = item['end_timestamp']
                dungeon.group = item['group']
                dungeon.server = item['server']

                if dungeon.server == "NA":
                    if Dungeon.objects.filter(name=dungeon.name).exists():
                        d_id = Dungeon.objects.filter(name=dungeon.name)[0].dungeonID
                        dungeon.dungeon_id = d_id

                dungeon.save()
