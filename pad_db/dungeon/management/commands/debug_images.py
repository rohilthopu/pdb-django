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
            card_id = json.loads(encounter_data.last())[-1]['card_id']
            print(card_id)
