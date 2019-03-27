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
            if encounter_data.last() is not None:
                boss = encounter_data.last().encounter_data

                card_id = json.loads(boss)[-1]['card_id']
                print(card_id)
