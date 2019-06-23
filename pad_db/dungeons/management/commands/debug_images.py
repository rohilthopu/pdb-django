from ...models import EncounterSet, Dungeon, Floor
from django.core.management.base import BaseCommand
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        encounters = EncounterSet.objects.all()
        dungeons = Dungeon.objects.all()
        floors = Floor.objects.all()

        for dungeon in dungeons:
            encounter_data = encounters.filter(dungeon_id=dungeon.dungeonID)
            dungeon_floors = floors.filter(dungeonID=dungeon.dungeonID)

            if encounter_data.last() is not None:
                boss = encounter_data.last().encounter_data

                card_id = json.loads(boss)[-1]['card_id']
                dungeon.imageID = card_id
                dungeon.save()

                for floor in dungeon_floors:
                    boss = encounter_data.filter(floor_id=floor.floorNumber)
                    if boss is not None and boss.last() is not None:
                        card_id = json.loads(boss.last().encounter_data)[-1]['card_id']
                        floor.imageID = card_id
                        floor.save()
