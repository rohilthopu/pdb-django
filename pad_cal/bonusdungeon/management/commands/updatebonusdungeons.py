from django.core.management.base import BaseCommand
from bonusdungeon.models import Dungeon
import requests
import json
import time
from datetime import datetime as dt


class Command(BaseCommand):

    def handle(self, *args, **options):

        for d in Dungeon.objects.all():
            d.delete()

        link = "https://storage.googleapis.com/mirubot/paddata/processed/na_bonuses.json"
        jsonPull = requests.get(link).text
        jsonLoad = json.loads(jsonPull)

        for item in jsonLoad:

            if item['dungeon'] is not None:
                dungeon = item['dungeon']

                exists = Dungeon.objects.filter(name=dungeon['clean_name'], startTime=item['start_timestamp']).first()

                if exists is None:

                    bonusDungeon = Dungeon()
                    bonusDungeon.name = dungeon['clean_name']
                    bonusDungeon.dungeonID = dungeon['dungeon_id']
                    bonusDungeon.startTime = item['start_timestamp']
                    bonusDungeon.endTime = item['end_timestamp']


                    # bonus data

                    bonus = item['bonus']

                    bonusDungeon.bonusName = bonus['bonus_name']
                    bonusDungeon.bonusStart = bonus['start_time_str']
                    bonusDungeon.bonusEnd = bonus['end_time_str']


                    bonusDungeon.save()


        dungeons = Dungeon.objects.all()

        for d in dungeons:

            start = dt.fromtimestamp(d.startTime)
            end = dt.fromtimestamp(d.endTime)
            now = dt.now()

            if time.time() >= d.endTime:
                print(d.name, dt.fromtimestamp(d.endTime))

            # if now.month == startData.month and now.month == endData.month and now.day in range(startData.day, endData.day):
            #     print(d.name, now.month, now.day)
