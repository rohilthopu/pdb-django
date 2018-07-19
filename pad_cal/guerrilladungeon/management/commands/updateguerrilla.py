from django.core.management.base import BaseCommand
import requests
import json
import time
from datetime import datetime

from guerrilladungeon.models import GuerrillaDungeon


class Command(BaseCommand):
    help = "Updates the Guerrilla Dungeon List."

    def handle(self, *args, **options):

        link = "https://storage.googleapis.com/mirubot/paddata/merged/guerrilla_data.json"
        jsonPull = requests.get(link).text
        jsonDump = json.loads(jsonPull)


        for d in GuerrillaDungeon.objects.all():
            d.delete()


        for item in jsonDump['items']:

            if GuerrillaDungeon.objects.filter(startTime=item['start_timestamp']).first() is None:
                dungeon = GuerrillaDungeon()

                dungeon.name = item['dungeon_name']
                dungeon.startTime = datetime.fromtimestamp(item['start_timestamp']).strftime("%A, %B %d, %Y %H:%M:%S")
                dungeon.endTime = datetime.fromtimestamp(item['end_timestamp']).strftime("%A, %B %d, %Y %H:%M:%S")
                dungeon.group = item['group']
                dungeon.server = item['server']
                dungeon.save()
