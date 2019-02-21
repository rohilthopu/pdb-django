from django.core.management.base import BaseCommand
import json
from dungeon.models import EncounterSet
import time
import os
from .dungeon_wave_parser import parse_spawn_data


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Starting Dungeon encounter build.'))

        start = time.time()

        EncounterSet.objects.all().delete()

        # call my wave parser to write to file
        parse_spawn_data.parse_waves()

        with open(os.path.abspath('/home/rohil/data/pad_data/processed_data/wave_data.json'), 'r') as jsonData:
            wave_data = json.load(jsonData)

        for item in wave_data:

            for floor in item['floors']:

                for wave in floor['waves']:
                    encounter_set = EncounterSet()

                    encounter_set.dungeon_id = item['dungeon_id']
                    encounter_set.floor_id = floor['floor']
                    encounter_set.wave_number = wave['wave']
                    encounter_set.encounter_data = json.dumps(wave['encounter_list'])
                    encounter_set.save()

        end = time.time()
        self.stdout.write(self.style.SUCCESS('Encounter update complete.'))
        print("Elapsed time :", end - start)
